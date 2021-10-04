import asyncio, threading
import sys, os, time, math
from subprocess import Popen, PIPE, DEVNULL
import tempfile

ffplay_cmd = "ffplay" # Assume it's on path and executable
statmatch = (8, "M-A:  0.000")

class AudioPlayer:
	def __init__(self):
		self._process = None
		self._thread = None
		self._position = 0
		self._position_start = 0
		self._position_updated_at = time.perf_counter()
		self._position_last_get = 0
		self._is_playing = False

	def _play(self, filepath, start=0):
		logfile_fd, logfile_loc = tempfile.mkstemp(prefix="LEDMASKLOG_")
		self._position = self._position_start = start
		self._is_playing = True
		with open(logfile_fd) as logfile:
			my_env = os.environ.copy()
			my_env["FFREPORT"] = f"file='{logfile_loc}':level=32"
			command = [ffplay_cmd,"-hide_banner","-fflags","nobuffer","-flags","low_delay","-stats","-nodisp","-autoexit","-ss",str(start),filepath]
			p = Popen(command, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, env=my_env, text=True)
			self._process = p
			self._position_updated_at = time.perf_counter()
			self._last_smoothed_position = 0
			while p.poll() is None:
				l = str(logfile.readline()).rstrip()
				if l:
					if l[statmatch[0]:].startswith(statmatch[1]):
						self._position = max(0, float(l[:statmatch[0]].strip())) + start + 0.03
						self._position_updated_at = time.perf_counter()
				time.sleep(0.005) # Good enough resolution
			self._is_playing = False
		os.remove(logfile_loc)
		print("Cleaned up")
			
	def play(self, filepath, start=0):
		if self._thread is not None:
			return
			
		t = threading.Thread(target=self._play, args=(filepath, start))
		t.daemon = True
		self._thread = t
		self._position = self._position_start = start
		self._is_playing = True
		t.start()
		
	def stop(self):
		if self._process is not None:
			self._process.terminate()
			self._process = None
		if self._thread is not None:
			self._thread.join()
			self._thread = None
	
	def get_position(self):
		t = self._position_start
		if self._position > t:
			dt = time.perf_counter() - self._position_updated_at
			t = max(self._position_last_get, self._position + dt)
		self._position_last_get = t
		return t
	
	def is_playing(self):
		return self._is_playing

async def run(ap):
	ap.play("eat your apple.it", start=0)
	oldbeat = None
	while ap.is_playing():
		t = ap.get_position()-0
		#if t >= 1:
		#	break
		#print("gt %.3f" % t)
		bpm = 135
		beat = math.floor(t*bpm/60)
		beattext = ""
		if beat < 0:
			beattext = "."*(-beat)
		else:
			beattext = "%3d:%1d" % ((beat//4)+1, (beat%4)+1)
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