from tkinter import Frame, Label
from PIL import ImageTk, Image

from kys.models.students import Students


class Student_pictures:
    def __init__(self, students: Students):
        self.Frame
        self.pictures: {str: ImageTk} = {}