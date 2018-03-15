from __future__ import print_function
try:
	import Tkinter as tk
	import tkMessageBox
except:
	import tkinter as tk
	import tkinter.messagebox as tkMessageBox


from Loader import Loader
from FlatButton import FlatButton

TEXT = """
This program detects black frames.
The algorithm is based on the ultimate filtering of outliers.
The pixel is normal if it lies inside k * sigma threshold.
On the 1st step, it filters pixels with k = k_ult.
On the 2nd step, it filters pixels with k = k_out.
You can change k_ult and k_out.
The default parameters are k_ult = 10.0, k_out = 3.0.
Click 'process()' for processing.
"""

PIC = """
 -----------
|  _        |
| |_|       |
|     /\    |
|    /  \/\ |
|   /      \|
 -----------
"""


class MainPage(tk.Frame):

	def __init__(self, parent, controller):
		self.parent = parent
		self.controller = controller
		tk.Frame.__init__(self, parent)

		self.loader = Loader(self, controller.color_scheme, 'Loading', fontsize=24)
		self.loader.place(relx=0.5, rely=0.5, anchor='center')
		self.loader.start()

		self.description = tk.Label(self,
		                            text=TEXT,
		                            font=('Monaco', 13),
		                            fg=controller.color_scheme['comments'],
		                            justify=tk.LEFT
		                            )

		self.k_ult = tk.Label(self,
		                      text='k_ult =',
		                      font=('Monaco', 16),
		                      justify=tk.LEFT)
		self.k_out = tk.Label(self,
		                      text='k_out =',
		                      font=('Monaco', 16),
		                      justify=tk.LEFT)
		self.canvas = tk.Canvas(self, width=400, height=140)
		self.process = FlatButton(self.canvas,
		                          controller.color_scheme,
		                          '.process()',
		                          fontsize=30,
		                          target=lambda event: self.target())

		self.pic = tk.Label(self.canvas,
		                    text=PIC,
		                    font=('Monaco', 10),
		                    justify=tk.CENTER)

		self.k_ult_var = tk.StringVar()
		self.ultEntry = tk.Entry(self,
		                         width=5,
		                         font=('Monaco', 16),
		                         textvariable=self.k_ult_var,
		                         highlightthickness=0,
		                         borderwidth=0
		                         )
		self.k_ult_var.set('10.0')

		self.k_out_var = tk.StringVar()
		self.outEntry = tk.Entry(self,
		                         width=5,
		                         font=('Monaco', 16),
		                         textvariable=self.k_out_var,
		                         highlightthickness=0,
		                         borderwidth=0
		                         )
		self.k_out_var.set('3.0')




	def show_config(self):
		self.loader.stop()
		self.loader.place_forget()
		self.description.place(x=50, y=20, anchor='nw')

		self.k_ult.place(x=50, rely=0.5, anchor='w')
		self.ultEntry.place(x=130, rely=0.5, anchor='w')
		self.k_out.place(x=250, rely=0.5, anchor='w')
		self.outEntry.place(x=330, rely=0.5, anchor='w')

		self.canvas.place(x=50, rely=0.8, anchor='w')
		self.process.place(x=80, rely=0.5, anchor='w')
		self.pic.place(x=0, y=110, anchor='sw')

	def target(self):
		k_out = None
		k_ult = None
		try:
			k_out = float(self.k_out_var.get())
			k_ult = float(self.k_ult_var.get())
		except:
			BaseException
			tkMessageBox.showerror(title="Wrong parameters", message="The parameters should be numbers.")
		if k_out and k_ult:
			self.controller.prepare_process(k_ult, k_out)

