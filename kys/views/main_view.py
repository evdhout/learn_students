from tkinter import Tk, StringVar, BOTTOM, TOP, Button
from tkinter import ttk
from PIL import Image, ImageTk
import os


class MainView:
    def __init__(self):
        self.root = Tk()
        self.root.title("KYS - Know Your Students!")

        # bound variables
        self.loading_status: StringVar = StringVar()
        self.loading_status.set("Loading configuration")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label = ttk.Label(self.mainframe, textvariable=self.loading_status).grid(column=0, row=1)

        self.mc_button_image: Image = Image.open('resources/kys-mc-button.png')
        self.mc_button_image_tk: ImageTk = ImageTk.PhotoImage(self.mc_button_image, master=self.root)
        self.button_play_mc = Button(self.mainframe, text="MC Quiz", image=self.mc_button_image_tk,
                                     compound=TOP)

        self.button_play_mc.grid(column=0, row=2)
        self.button_play_mc.grid(column=1, row=2)
