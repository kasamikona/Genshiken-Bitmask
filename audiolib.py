import asyncio, threading
import sys, os, time, math
from subprocess import Popen, PIPE, DEVNULL, STDOUT

ffplay_cmd = "ffplay" # Assume it's on path and executable
ffmpeg_cmd = "ffmpeg"
hw_latency = 0.1 # Around 100ms on typical hardware?
audfmt = "-f s16le -ar 44100 -ac 2" # 16bit 44100Hz stereo
audfmt_bytes = 4

class AudioPlayer:
	def __init__(self):
		self._process_read = None
		self._process_play = None
		self._thread = None
		self._position = 0
		self._position_updated_at = time.perf_counter()
		self._position_last_get = 0
		self._is_playing = False

	def _play(self, filepath, env=None):
		mixenv = os.environ.copy()
		mixenv.update(env or {})
		self._position = 0
		self._is_playing = True
		pipe_read, pipe_write = os.pipe()
		noout = "-hide_banner -loglevel quiet"
		cmd_read = f"{ffmpeg_cmd} {noout} -i".split()+[filepath]+f"{audfmt} pipe:1".split()
		cmd_play = f"{ffplay_cmd} {noout} {audfmt} -nodisp -autoexit -probesize 32 -".split()
		process_play = Popen(cmd_play, stdout=None, stderr=None, stdin=PIPE, env=mixenv)
		process_read = Popen(cmd_read, stdout=pipe_write, stderr=None, stdin=DEVNULL, env=mixenv)
		self._process_read = process_read
		self._process_play = process_play
		self._position_updated_at = time.perf_counter()
		self._last_smoothed_position = 0
		nextbuftime = time.perf_counter()
		tcnt = 0
		while process_read.poll() is None:
			tnow = time.perf_counter()
			if tnow > nextbuftime:
				nextbuftime += 200/44100
				try:
					b = os.read(pipe_read, 200*audfmt_bytes)
					tcnt += len(b)/4
					process_play.stdin.write(b)
					process_play.stdin.flush()
					self._position = (tcnt+200*audfmt_bytes)/44100
					self._position_updated_at = tnow
				except Exception:
					pass
			time.sleep(1/500)
		time.sleep(0.2)
		self._is_playing = False
			
	def play(self, filepath, env=None):
		if self._thread is not None:
			return
			
		t = threading.Thread(target=self._play, args=(filepath,env))
		t.daemon = True
		self._thread = t
		self._position = 0
		self._is_playing = True
		t.start()
		
	def stop(self):
		if self._process_read.poll() is None:
			self._process_read.terminate()
		if self._process_play.poll() is None:
			self._process_play.terminate()
		if self._thread is not None:
			self._thread.join()
			self._thread = None
	
	def get_position(self):
		t = -hw_latency
		if self._position > 0:
			dt = time.perf_counter() - self._position_updated_at
			t = max(self._position_last_get, self._position + dt - hw_latency)
		self._position_last_get = t
		return t
	
	def is_playing(self):
		return self._is_playing

async def run(ap):
	ap.play("eat your apple.it", env={"SDL_AUDIODRIVER":"wasapi"})
	oldbeat = None
	while ap.is_playing():
		t = ap.get_position()
		#print(t)
		bpm = 135
		beat = math.floor(t*bpm/60)
		beattext = ""
		if beat < 0:
			beattext = "/"*(-beat)
		else:
			beattext = "%3d %s|" % (beat+1, "  "*(beat%4))
		if beattext != oldbeat:
			print("Beat %s" % beattext)
			oldbeat = beattext
		await asyncio.sleep(0.01)
	ap.stop()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	ap = AudioPlayer()
	try:
		asyncio.run(run(ap))
	except KeyboardInterrupt as e:
		print("Caught keyboard interrupt")
		ap.stop()
		#time.sleep(0.1)
	finally:
		loop.close()