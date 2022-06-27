class Scene:
	def __init__(self):
		self.layers = {}
		self.effects = {}
		self.effects_tstart = {}
		self.loop_actions = []
		self.frame_count = 0
		self.final_layer = None
		self.music = None

	def render(self, t_global):
		for action in self.loop_actions:
			self.oneshot(action[0], action[1], action[2], t_global)
		self.frame_count += 1
		if self.final_layer is not None and self.final_layer in self.layers:
			return self.layers[self.final_layer]

	def oneshot(self, index_out, name_effect, indexes_ins, t_global):
		effect = self.effects[name_effect]
		t_effect = t_global - self.effects_tstart[name_effect]
		out = self.layers[index_out]
		ins = [self.layers[x] for x in indexes_ins]
		effect.render(out, ins, t_global, self.frame_count, t_effect)

	def add_effect(self, name_effect, effect, tstart=0):
		self.remove_effect(name_effect)
		self.effects[name_effect] = effect
		self.effects_tstart[name_effect] = tstart

	def remove_effect(self, name_effect):
		if name_effect in self.effects:
			self.effects.pop(name_effect).cleanup()
			del self.effects_tstart[name_effect]

	def clear_effects(self):
		for name_effect in self.effects:
			self.effects[name_effect].cleanup()
		self.effects.clear()

	def add_layer(self, name_layer, layer):
		self.remove_layer(name_layer)
		self.layers[name_layer] = layer

	def remove_layer(self, name_layer):
		if name_layer in self.layers:
			self.layers.pop(name_layer).cleanup()

	def clear_layers(self):
		for name_layer in self.layers:
			self.layers[name_layer].cleanup()
		self.layers.clear()

	def play_music(self, filename, loop=False):
		if self.music:
			self.music.stop()
		self.music = Music(filename, loop)

	def stop_music(self):
		if self.music:
			self.music.stop()
			self.music = None

	def cleanup(self):
		self.stop_music()
		self.clear_effects()
		self.loop_actions.clear()

class Layer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.buffer = [[0]*height for i in range(width)]
	
	def cleanup(self):
		del self.buffer # idk if it would GC, could memory leak large arrays

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

import shlex
class SceneAnimator:
	def __init__(self, story_filename, effect_classes):
		self.story_file = open(story_filename)
		self.ended = False
		self.available_effects = {}
		for ec in effect_classes:
			self.available_effects[ec.__name__] = ec
		self.time_waiting = 0
		self.scene = Scene()
		self.sub_parser = None

	def update(self, t):
		if self.time_waiting < 0 or self.ended:
			return False
		while t >= self.time_waiting:
			if not self._process_next(self.time_waiting):
				break
		return True

	def render(self, t):
		return self.scene.render(t)

	def cleanup(self):
		if not self.ended:
			self.ended = True
			self.scene.cleanup()
			self.story_file.close()

	def _parse_time(self, s):
		# seconds or minutes:seconds
		# beats,bpm or bars:beats,bpm (4 beats per bar)
		# bars:beats,bpm,n (n beats per bar)
		# minutes and bars must be integers, seconds and beats can have decimals.
		parts = s.split("/")
		if len(parts) == 0:
			return 0
		try:
			time_str = parts[0].split(":")
			mins = 0
			secs = 0
			if len(time_str) > 1:
				mins = int(time_str.pop(0))
			secs = float(time_str[0])
			scale = 1
			mins_ratio = 60 # 60 seconds : 1 minute
			if len(parts) > 1:
				scale = 60/int(parts[1]) # beats per minute -> seconds per beat
				mins_ratio = 4 # 4 beats : 1 bar
				if len(parts) > 2:
					mins_ratio = int(parts[2]) # n beats : 1 bar
			return (secs+(mins_ratio*mins))*scale
		except ValueError:
			return 0

	def _process_next(self, at_time):
		current_offset = self.story_file.tell()
		line = self.story_file.readline()
		if line == "":
			self.cleanup()
			return False
		tokens = shlex.split(line, comments=True, posix=True)
		return self._process_tokens(tokens, at_time)

	def _process_tokens(self, tokens, at_time):
		if self.sub_parser == "loop":
			return self._process_tokens_loop(tokens, at_time)
		return self._process_tokens_normal(tokens, at_time)

	def _process_tokens_normal(self, tokens, at_time):
		if len(tokens) == 0:
			return True

		command = tokens.pop(0).lower()
		if command == "at":
			waittime = self._parse_time(tokens.pop(0))
			if waittime > at_time:
				self.time_waiting = waittime
				return False
		elif command == "playmus":
			musfile = tokens.pop(0)
			self.scene.play_music(musfile)
		elif command == "stopmus":
			self.scene.stop_music()
		elif command == "clreffects":
			self.scene.clear_effects()
		elif command == "clrlayers":
			self.scene.clear_layers()
		elif command == "addeffect":
			effectname = tokens.pop(0)
			effectclass = tokens.pop(0)
			effectargs = [(float(x) if x.isnumeric() else x) for x in tokens]
			if not effectclass in self.available_effects:
				print("Unknown effect class:", effectclass)
				return True
			effectinstance = self.available_effects[effectclass](*effectargs)
			self.scene.add_effect(effectname, effectinstance, at_time)
		elif command == "deleffect":
			self.scene.remove_effect(tokens.pop(0))
		elif command == "addlayer":
			layername = tokens.pop(0)
			layerwidth = int(tokens.pop(0))
			layerheight = int(tokens.pop(0))
			self.scene.add_layer(layername, Layer(layerwidth, layerheight))
		elif command == "dellayer":
			self.scene.remove_layer(tokens.pop(0))
		elif command == "draw":
			layerout = tokens.pop(0)
			effectname = tokens.pop(0)
			layersin = tokens
			self.scene.oneshot(layerout, effectname, layersin, at_time)
		elif command == "output":
			self.scene.final_layer = tokens.pop(0)
		elif command == "loop":
			self.scene.loop_actions.clear()
			self.sub_parser = "loop"
		else:
			print("Unknown story command:", command)
			return True

		return True
	
	def _process_tokens_loop(self, tokens, at_time):
		if tokens[0].lower() == "loopend":
			self.sub_parser = None
			return True
		layerout = tokens.pop(0)
		effectname = tokens.pop(0)
		layersin = tokens
		action = (layerout,effectname,layersin)
		self.scene.loop_actions.append(action)
		return True