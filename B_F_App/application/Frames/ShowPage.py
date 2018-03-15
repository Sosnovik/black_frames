from __future__ import print_function
import numpy as np
try:
	import Tkinter as tk
	import tkFileDialog
	import tkMessageBox
except:
	import tkinter as tk
	import tkinter.filedialog  as tkFileDialog
	import tkinter.messagebox as tkMessageBox

from Loader import Loader
from FlatButton import FlatButton
from PIL import ImageTk


MESSAGE = """Do you want to save indices for square array?
If not, it would be saved for linear array.
"""

def save_indices(root, controller):
	answer = tkMessageBox.askquestion(title='Save indices', message=MESSAGE)
	if answer == 'yes':
		d = 2
	else:
		d = 1
	fn = tkFileDialog.SaveAs(root, filetypes = [('*.txt files', '.txt')]).show()
	if not fn == '':
		if d == 1:
			np.savetxt(fn, controller.model.all_indices(d=d), fmt='%d')
		else:
			np.savetxt(fn, controller.model.all_indices(d=d), fmt='%d %d')


def recompute(controller):
	controller.show_process_page()


def new_images(controller):
	controller.model = None
	controller.start()


class ShowPage(tk.Frame):

	def __init__(self, parent, controller):
		self.parent = parent
		self.controller = controller
		self.images = None
		self.n_image = 0
		tk.Frame.__init__(self, parent)

		self.loader = Loader(self, controller.color_scheme, 'Processing', fontsize=24)
		self.loader.place(relx=0.5, rely=0.5, anchor='center')
		self.loader.start()

		self.menu = tk.Canvas(self, width=150)
		self.save_indices_button = FlatButton(self.menu, controller.color_scheme, 'Save indices', 16, lambda x: save_indices(self, controller))
		self.recompute_button = FlatButton(self.menu, controller.color_scheme, 'Recompute', 16, lambda x: recompute(self.controller))
		self.new_images_button = FlatButton(self.menu, controller.color_scheme, 'New images', 16, lambda x: new_images(self.controller))

		self.view = tk.Canvas(self)
		self.image_view = tk.Label(self.view)

		self.controls = tk.Canvas(self, height=80, width=100)
		self.next_button = FlatButton(self.controls, controller.color_scheme, '>', 30, lambda x: self.show_next())
		self.prev_button = FlatButton(self.controls, controller.color_scheme, '<', 30, lambda x: self.show_prev())

	def show_pics(self):
		self.loader.stop()
		self.loader.place_forget()
		self.images = [f.pil_out for f in self.controller.model.filters]

		self.menu.pack(side='left', fill='both')
		self.save_indices_button.place(x=20, y=20, anchor='nw')
		self.recompute_button.place(x=20, y=60, anchor='nw')
		self.new_images_button.place(x=20, y=100, anchor='nw')

		self.view.pack(fill='both', expand=1)
		image = ImageTk.PhotoImage(self.images[self.n_image])
		self.image_view.configure(image=image)
		self.image_view.image = image
		self.image_view.pack(fill='both', expand=1)

		self.controls.pack(side='bottom')
		self.next_button.place(x=75, rely=0.5, anchor='center')
		self.prev_button.place(x=25, rely=0.5, anchor='center')

	def show_next(self):
		if self.n_image < len(self.images) - 1:
			self.n_image += 1
			image = ImageTk.PhotoImage(self.images[self.n_image])
			self.image_view.configure(image=image)
			self.image_view.image = image

	def show_prev(self):
		if self.n_image > 0:
			self.n_image -= 1
			image = ImageTk.PhotoImage(self.images[self.n_image])
			self.image_view.configure(image=image)
			self.image_view.image = image
