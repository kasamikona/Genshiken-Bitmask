class Scene:
	def __init__(self):
		self.layers = []
		self.events = []
		self.compositing_list = []
		self.frame_count = 0
		self.final_layer = 0

	def render(self, t_global):
		for action in self.compositing_list:
			# (index_event, index_out, index_ins)
			event = self.events[action[0]]
			out = self.layers[action[1]]
			ins = [self.layers[x] for x in action[2]]
			event.render(out, ins, t_global, self.frame_count)

		self.frame_count += 1

		if self.final_layer >= 0:
			return self.layers[self.final_layer]

class Layer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.buffer = [[0]*height for i in range(width)]

class Effect:
	def __init__(self):
		pass

	def render(self, out, ins, t_global, t_global_f, t_event):
		pass

class Event:
	def __init__(self, effect, t_start):
		self.effect = effect
		self.t_start = t_start

	def render(self, out, ins, t_global, t_global_f):
		self.effect.render(out, ins, t_global, t_global_f, t_global+self.t_start)
