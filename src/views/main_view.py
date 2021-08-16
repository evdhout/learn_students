import sys
import platform
from tkinter import Tk, messagebox, TOP, EW, NSEW
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Callable
from src.models.configuration import Configuration


class MainView:
    def __init__(self, config: Configuration):
        self.config: Configuration = config
        self.root = Tk()
        self.root.title(_("KYS - Know Your Students!"))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # use classic theme if not on windows
        if platform.system != 'Windows':
            ttk.Style().theme_use('classic')

        try:
            self.mc_button_image: Image = Image.open(self.config.get_resource_path('resources/kys-mc-button.png'))
            self.type_button_image: Image = Image.open(self.config.get_resource_path('resources/kys-type-button.png'))
        except OSError as e:
            messagebox.showerror(
                message=_('Error opening button image'),
                title=_('Fatal error'),
                icon='error',
                detail=str(e))
            sys.exit()

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)

        self.select_group_button = ttk.Button(self.mainframe, text=_('Select Group'))
        self.select_group_button.grid(column=0, row=0, columnspan=2, sticky=EW)

        self.mc_button_image_tk: ImageTk = ImageTk.PhotoImage(self.mc_button_image, master=self.root)
        self.mc_button = ttk.Button(self.mainframe, text=_("Multiple Choice Quiz"),
                                    image=self.mc_button_image_tk, compound=TOP)
        self.mc_button.grid(column=0, row=10, sticky=NSEW)

        self.type_button_image_tk: ImageTk = ImageTk.PhotoImage(self.type_button_image, master=self.root)
        self.type_button = ttk.Button(self.mainframe, text=_("Type Quiz"),
                                      image=self.type_button_image_tk, compound=TOP)
        self.type_button.grid(column=1, row=10, sticky=NSEW)

        self.deactivate_buttons()

    def mainloop(self):
        self.root.mainloop()

    def bind_buttons(self, mc_callback: Callable, type_callback: Callable, group_callback: Callable):
        self.mc_button.config(command=mc_callback)
        self.type_button.config(command=type_callback)
        self.select_group_button.config(command=group_callback)

    def set_group_name(self, group_name):
        self.select_group_button.configure(text=_('Group: {}').format(group_name))
        self.activate_buttons()

    def bind_after_load(self, callback: Callable):
        self.root.bind('<Map>', lambda e: callback())

    def after_load_done(self):
        self.root.unbind('<Map>')
        self.activate_buttons()

    def deactivate_buttons(self):
        self.mc_button.state(['disabled', '!active', '!focus', '!hover'])
        self.type_button.state(['disabled', '!active', '!focus', '!hover'])

    def activate_buttons(self):
        self.mc_button.state(['!disabled', '!active', '!focus', '!hover'])
        self.type_button.state(['!disabled', '!active', '!focus', '!hover'])
