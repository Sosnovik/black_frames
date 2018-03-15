from __future__ import print_function
try:
	import Tkinter as tk
	import tkFileDialog
except:
	import tkinter as tk
	import tkinter.filedialog as tkFileDialog

from FlatButton import FlatButton


class StartPage(tk.Frame):
	LABEL_FONT = ('Monaco', 30)
	LABEL_TEXT = 'LOAD IMAGES'

	def __init__(self, parent, controller):
		self.controller = controller
		tk.Frame.__init__(self, parent)
		self.load_button = FlatButton(self,
		                              controller.color_scheme,
		                              self.LABEL_TEXT,
		                              30,
		                              lambda event: self.load_files())
		self.load_button.place(relx=0.5, rely=0.5, anchor='center')

	def load_files(self):
		files = tkFileDialog.askopenfilenames(parent=self.controller, title='Choose images')
		if not files == "":
			paths = [path for path in files]
			self.controller.load_files(paths)
