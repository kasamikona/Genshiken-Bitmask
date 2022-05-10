class Scene:
	def __init__(self):
		self.layers = []
		self.effects = []
		self.compositing_list = []
		self.frame_count = 0
		self.final_layer = 0

	def render(self, t_global):
		for action in self.compositing_list:
			# (index_effect, index_out, index_ins)
			effect = self.effects[action[0]]
			out = self.layers[action[1]]
			ins = [self.layers[x] for x in action[2]]
			effect.render(out, ins, t_global, self.frame_count, t_global)

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

	def render(self, out, ins, t_global, t_global_f, t_effect):
		pass
