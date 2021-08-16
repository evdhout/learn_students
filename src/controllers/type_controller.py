from src.models.students import Students
from src.views.main_view import MainView
from src.views.type_view import TypeView
from src.controllers.quiz_controller import QuizController


class TypeController(QuizController):
    def __init__(self, master: MainView, students: Students):
        super().__init__(master=master, students=students)

        self.quiz_view: TypeView = TypeView(self.master, start_command=self.start_quiz,
                                            next_command=self.show_next_student,
                                            enter_command=self.check_student_name)

    def show_next_student(self):
        super().show_next_student()

        if self.current_student is None:
            return

        self.quiz_view.ask_question()

    def check_student_name(self):
        typed_name = self.quiz_view.get_name_entry_value()
        # print(typed_name)
        if typed_name.lower() == self.current_student.first_name.lower():
            self.total_correct_names += 1
            result = True
        else:
            self.total_wrong_names += 1
            result = False

        self.quiz_view.show_student_result(result=result,
                                           student_name=self.current_student.get_full_name(),
                                           correct=self.total_correct_names,
                                           wrong=self.total_wrong_names)
