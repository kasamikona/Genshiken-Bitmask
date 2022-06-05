class Scene:
	def __init__(self):
		self.layers = []
		self.effects = {}
		self.compositing_list = []
		self.frame_count = 0
		self.final_layer = 0
		self.music = None

	def render(self, t_global):
		for action in self.compositing_list:
			# (name_effect, indexes_ins, index_out)
			effect = self.effects[action[0]]
			out = self.layers[action[2]]
			ins = [self.layers[x] for x in action[1]]
			effect.render(out, ins, t_global, self.frame_count, t_global)

		self.frame_count += 1

		if self.final_layer >= 0:
			return self.layers[self.final_layer]

	def add_effect(self, name_effect, effect):
		self.remove_effect(name_effect)
		self.effects[name_effect] = effect

	def remove_effect(self, name_effect):
		if name_effect in self.effects:
			self.effects.pop(name_effect).cleanup()

	def play_music(self, filename, loop=False):
		if self.music:
			self.music.stop()
		self.music = Music(filename, loop)

	def stop_music(self):
		if self.music:
			self.music.stop()
			self.music = None

	def cleanup(self):
		for name_effect in self.effects:
			self.effects[name_effect].cleanup()
		self.effects = {}
		self.stop_music()

class Layer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.buffer = [[0]*height for i in range(width)]

class Effect:
	def __init__(self):
		pass

	def render(self, out, ins, t_global, t_global_f, t_effect):
		pass

	def cleanup(self):
		pass

from subprocess import Popen, PIPE, DEVNULL
class Music:
	def __init__(self, filename, loop=False):
		self.command = ["ffplay","-nodisp","-hide_banner","-loop",("0" if loop else "1"),filename]
		self.mproc = Popen(self.command, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)

	def stop(self):
		if self.mproc:
			self.mproc.terminate()
			self.mproc = None