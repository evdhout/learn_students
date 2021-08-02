from PIL import Image, ImageTk
from kys.controllers.mc_controller import MCController
from kys.controllers.students_csv import StudentsCSV
from kys.models.configuration import Configuration
from kys.models.students import Students
from kys.views.main_view import MainView


class MainController:
    def __init__(self, students: Students, config: Configuration):
        self.students = students
        self.config = config
        self.quiz_controller = None

        self.main_view: MainView = MainView()
        self.main_view.bind_mc_button(self.open_mc_window)
        self.main_view.bind_after_load(self.load_students)
        self.main_view.mainloop()

    def load_students(self):
        _ = StudentsCSV(students=self.students, config=self.config)
        for student in self.students:
            image: Image = Image.open(student.picture_path)
            student.image = ImageTk.PhotoImage(image, master=self.main_view.root)
            self.main_view.update_loading_status(f"{student.get_full_name()} image loaded")
        self.main_view.update_loading_status(f"Loaded {len(self.students)} students")
        self.main_view.after_load_done()

    def open_mc_window(self):
        self.quiz_controller = MCController(self.main_view, students=self.students)
