from tkinter import Tk, StringVar, TOP, Button
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Callable


class MainView:
    def __init__(self):
        self.root = Tk()
        self.root.title("KYS - Know Your Students!")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mc_button_image: Image = Image.open('resources/kys-mc-button.png')
        self.mc_button_image_tk: ImageTk = ImageTk.PhotoImage(self.mc_button_image, master=self.root)
        self.mc_button = Button(self.mainframe, text="Multiple Choice Quiz", image=self.mc_button_image_tk, compound=TOP)

        self.type_button_image: Image = Image.open('resources/kys-type-button.png')
        self.type_button_image_tk: ImageTk = ImageTk.PhotoImage(self.type_button_image, master=self.root)
        self.type_button = Button(self.mainframe, text="Type Quiz", image=self.type_button_image_tk, compound=TOP)

        self.mc_button.grid(column=1, row=2)
        self.type_button.grid(column=2, row=2)

    def mainloop(self):
        self.root.mainloop()

    def bind_buttons(self, mc_callback: Callable, type_callback: Callable):
        self.mc_button.config(command=mc_callback)
        self.type_button.config(command=type_callback)

    def bind_after_load(self, callback: Callable):
        self.root.bind('<Map>', lambda e: callback())

    def after_load_done(self):
        self.root.unbind('<Map>')
