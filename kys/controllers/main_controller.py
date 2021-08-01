from tkinter import Toplevel
from PIL import Image, ImageTk
import time
from kys.models.student import Student
from kys.models.students import Students
from kys.views.main_view import MainView
from kys.controllers.mc_controller import MCController
from kys.controllers.students_csv import StudentsCSV
from kys.models.configuration import Configuration


class MainController:
    def __init__(self, students: Students, config: Configuration):
        self.students = students
        self.config = config
        self.view = MainView()
        self.view.button_play_mc.configure(command=self.open_mc_window)
        self.sub_window = None
        self.sub_controller = None

        self.view.root.bind('<Map>', self.load_students)
        self.view.root.mainloop()

    def load_students(self, event):
        students_csv = StudentsCSV(students=self.students, config=self.config, status=self.view.loading_status)
        for student in self.students:
            image: Image = Image.open(student.picture_path)
            student.image = ImageTk.PhotoImage(image, master=self.view.root)
            self.view.loading_status.set(f"{student.get_full_name()} image loaded")
        self.view.loading_status.set(f"Loaded {len(self.students)} students")
        self.view.root.unbind('<Map>')

    def open_mc_window(self):
        self.sub_window = Toplevel(self.view.root)
        self.sub_controller = MCController(self.sub_window, students=self.students)
