import configparser
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from kys.controllers.mc_controller import MCController
from kys.controllers.type_controller import TypeController
from kys.controllers.students_csv import StudentsCSV
from kys.models.configuration import Configuration
from kys.models.students import Students
from kys.views.main_view import MainView


class MainController:
    def __init__(self, config: Configuration):
        self.students = Students()
        self.config = config
        self.quiz_controller = None
        self.initial_ini_read = False

        self.main_view: MainView = MainView()
        self.main_view.bind_buttons(mc_callback=self.open_mc_window,
                                    type_callback=self.open_type_window,
                                    group_callback=self.load_group)
        if self.config.config_read:
            self.main_view.bind_after_load(self.load_students)
            self.initial_ini_read = True
        self.main_view.mainloop()

    def load_students(self):
        _ = StudentsCSV(students=self.students, config=self.config)
        for student in self.students:
            image: Image = Image.open(student.picture_path)
            student.image = ImageTk.PhotoImage(image, master=self.main_view.root)
            if self.initial_ini_read:
                self.initial_ini_read = False
                self.main_view.after_load_done()
                self.main_view.set_group_name(group_name=self.config.kys.get('group_name',
                                                                             Path(self.config.config_file).stem))

    def load_group(self):
        group_file = filedialog.askopenfilename(filetypes=[(_('Group File'), ".ini")],
                                                title=_('Select group ini file'))
        if not group_file:
            return

        try:
            real_group_file = self.config.file_exists(group_file)
            self.config.parse_ini(real_group_file)
        except FileNotFoundError as e:
            messagebox.showerror(message=_('Group file {} does not exist').format(group_file),
                                 title=_('Group init error'),
                                 icon='error',
                                 detail=str(e))
            return
        except configparser.NoSectionError as e:
            messagebox.showerror(message=_('Section in group file {} does not exist').format(group_file),
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
