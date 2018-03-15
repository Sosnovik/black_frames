try:
	import Tkinter as tk
except:
	import tkinter as tk
import threading
from time import sleep


class StoppableThread(threading.Thread):
	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self, *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()


class Loader(tk.Label):

	#sequence = ['-', '\\', '|', '/']
	sequence = ['.  ', '.. ', '...']

	def __init__(self, parent, color_scheme, text, fontsize):
		self.text_ = text
		self.textVar = tk.StringVar()
		self.textVar.set(self.text_  + self.sequence[-1])
		tk.Label.__init__(self, parent, textvariable=self.textVar, font=('Monaco', fontsize), fg=color_scheme['comments'])
		self.thread = None
		self.continue_ = True

	def start(self):

		def loop():
			i = 0
			while self.continue_:
				sleep(0.3)
				self.textVar.set(self.text_  + self.sequence[i])
				i += 1
				i %= len(self.sequence)

		self.thread = StoppableThread(target=loop)
		self.thread.start()

	def stop(self):
		self.continue_ = False
		self.thread.stop()