try:
	import Tkinter as tk
except:
	import tkinter as tk


class FlatButton(tk.Label):

	def __init__(self, parent, color_scheme, text, fontsize, target):
		tk.Label.__init__(self, parent, text=text, font=('Monaco', fontsize), fg=color_scheme['comments'])
		self.bind('<Enter>', lambda event: self.config(fg=color_scheme['foreground']))
		self.bind('<Leave>', lambda event: self.config(fg=color_scheme['comments']))
		self.bind('<Button-1>', target)

