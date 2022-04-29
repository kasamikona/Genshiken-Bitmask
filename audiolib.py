import asyncio, threading
import sys, os, time, math
from subprocess import Popen, PIPE, DEVNULL

ffplay_cmd = "ffplay" # Assume it's on path and executable
statmatch = (8, "M-A:  0.000")
time_read_resolution = 0.01; # Good enough resolution for around 10fps
time_offset = 0.1; #

class AudioPlayer:
	def __init__(self):
		self.process = None
		self.thread = None
		self.position = 0
		self.position_start = 0
		self.position_updated_at = time.perf_counter()
		self.position_last_get = 0
		self.is_playing = False

	def runplay(self, filepath, start=0):
		self.position = self.position_start = start
		self.is_playing = True
		command = [ffplay_cmd,"-hide_banner","-fflags","nobuffer","-flags","low_delay","-stats","-nodisp","-autoexit","-ss",str(start),filepath]
		p = Popen(command, stdout=DEVNULL, stderr=PIPE, stdin=PIPE, text=True, encoding="utf8")
		self.process = p
		self.position_updated_at = time.perf_counter()
		self.last_smoothed_position = 0
		while p.poll() is None:
			l = str(p.stderr.readline()).rstrip()
			if l:
				if l[statmatch[0]:].startswith(statmatch[1]):
					#print(l);
					self.position = max(0, float(l[:statmatch[0]].strip())) + start + 0.1
					self.position_updated_at = time.perf_counter()
					time.sleep(time_read_resolution)
			else:
				time.sleep(time_read_resolution)
		self.is_playing = False
			
	def play(self, filepath, start=0):
		if self.thread is not None:
			return
			
		t = threading.Thread(target=self.runplay, args=(filepath, start))
		t.daemon = True
		self.thread = t
		self.position = self.position_start = start
		self.is_playing = True
		t.start()
		
	def stop(self):
		if self.process is not None:
			self.process.terminate()
			self.process = None
		if self.thread is not None:
			self.thread.join()
			self.thread = None
	
	def get_position(self):
		t = self.position_start
		if self.position > t:
			dt = time.perf_counter() - self.position_updated_at
			t = max(self.position_last_get, self.position + dt)
		self.position_last_get = t
		return t


async def run(ap):
	ap.play("yuzukoncept.xm", start=0)
	oldbeat = None
	while ap.is_playing:
		t = ap.get_position()
		bpm = 125
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
	loop = asyncio.new_event_loop()
	ap = AudioPlayer()
	try:
		asyncio.run(run(ap))
	except KeyboardInterrupt as e:
		print("Caught keyboard interrupt")
		ap.stop()
		#time.sleep(0.1)
	finally:
		loop.close()