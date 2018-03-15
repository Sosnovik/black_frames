from __future__ import print_function
try:
	import Tkinter as tk
except:
	import tkinter as tk

import tkMessageBox
import json
import threading

from Frames import StartPage, MainPage, ShowPage
from Models import JoinFilter


class App(tk.Tk):
	def __init__(self):
		with open('application/Resources/light', 'r') as scheme_file:
			self.color_scheme = json.load(scheme_file)
		self.font = 'Monaco'
		self.model = None
		tk.Tk.__init__(self)
		tk.Tk.update_idletasks(self)
		tk.Tk.wm_title(self, "Black Frames")
		tk.Tk.minsize(self, 800, 500)
		# self.add_menu()
		container = tk.Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.container = container
		self.update_colors()
		self.frames = {}
		self.paths = None
		self.page = None
		self.start()

	def start(self):
		self.show_frame('StartPage')

	def update_colors(self):
		self.tk_setPalette(
			background=self.color_scheme['background'],
			foreground=self.color_scheme['foreground']
		)

	def show_frame(self, frame_key):
		if frame_key == 'StartPage':
			self.page = StartPage(self.container, self)
		elif frame_key == 'MainPage':
			self.page = MainPage(self.container, self)
		elif frame_key == 'ShowPage':
			self.page = ShowPage(self.container, self)
		self.page.grid(row=0, column=0, sticky='news')

	# Preprocessing
	def load_files(self, paths):
		self.paths = paths
		self.show_process_page()

	def show_process_page(self):
		def success():
			self.page.show_config()

		def failure():
			tkMessageBox.showerror(title="Different shapes", message="Selected images have different shapes")

		def target(p, s=success, f=failure):
			self.model = JoinFilter(p, success=s, failure=f)

		self.show_frame('MainPage')
		if self.model:
			self.page.show_config()
			return
		thread = threading.Thread(
			target=lambda p, s, f: target(p, s, f),
			args=(self.paths, success, failure))
		thread.start()

	# Processing
	def prepare_process(self, k_ult, k_out):
		self.model.set_k_ult(k_ult)
		self.model.set_k_out(k_out)
		self.process()

	def process(self):
		self.show_frame('ShowPage')

		def success():
			self.model.mark(completion=lambda: self.page.show_pics())

		thread = threading.Thread(
			target=lambda s: self.model.process(s),
			args=([success]))
		thread.start()

	# Menu
	# def add_menu(self):
	# 	pass
