import configparser
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from src.controllers.mc_controller import MCController
from src.controllers.type_controller import TypeController
from src.controllers.students_csv import StudentsCSV
from src.models.configuration import Configuration
from src.models.students import Students
from src.views.main_view import MainView


class MainController:
    def __init__(self, config: Configuration):
        self.students = Students()
        self.config = config
        self.quiz_controller = None

        self.main_view: MainView = MainView(config=self.config)
        self.main_view.bind_buttons(mc_callback=self.open_mc_window,
                                    type_callback=self.open_type_window,
                                    group_callback=self.load_group)
        self.load_students()
        self.main_view.mainloop()

    def load_students(self):
        self.students = Students()
        try:
            StudentsCSV(students=self.students, config=self.config)
        except FileNotFoundError as e:
            messagebox.showerror(
                message=_('Student CSV file {} does not exist').format(Path(self.config.csv['student_csv']).stem),
                title=_('Error reading Students'),
                icon='error',
                detail=str(e))
            return
        for student in self.students:
            image: Image = Image.open(student.picture_path)
            student.image = ImageTk.PhotoImage(image, master=self.main_view.root)
        self.main_view.set_group_name(group_name=self.config.kys.get('group_name', '__CONFIG__'))

    def load_group(self):
        filename = filedialog.askopenfilename(filetypes=[(_('Group File'), ".ini")],
                                              title=_('Select group ini file'))
        group_file = self.config.get_resource_path(filename)
        if not self.config.file_exists(group_file):
            messagebox.showerror(message=_('Group file {} does not exist').format(Path(group_file).stem),
                                 title=_('Group init error'),
                                 icon='error',
                                 detail=group_file)
            return

        try:
            self.config.parse_ini(group_file)
        except configparser.NoSectionError as e:
            messagebox.showerror(message=_('Section in group file {} does not exist').format(Path(group_file).stem),
                                 title=_('Group section error'),
                                 icon='error',
                                 detail=str(e))
            return

        self.load_students()
        self.main_view.set_group_name(group_name=self.config.kys.get('group_name', Path(group_file).stem))

    def open_mc_window(self):
        self.quiz_controller = MCController(self.main_view, students=self.students)

    def open_type_window(self):
        self.quiz_controller = TypeController(self.main_view, students=self.students)
