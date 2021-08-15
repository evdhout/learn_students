from enum import Enum
from random import shuffle

from kys.models.student import Student
from kys.models.students import Students
from kys.views.mc_view import MCView
from kys.views.main_view import MainView
from kys.controllers.quiz_controller import QuizController


class ButtonStyle(Enum):
    NORMAL = "normal"
    CORRECT = "correct"
    WRONG = "wrong"


class MCController(QuizController):
    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_C = 2

    OPTION = {'A': 0, 'B': 1, 'C': 2, 'D': 4}

    def __init__(self, master: MainView, students: Students):
        super().__init__(master=master, students=students)

        self.quiz_view: MCView = MCView(self.master,
                                        start_command=self.start_quiz,
                                        next_command=self.show_next_student,
                                        choice_button_command=self.chosen_student_name)

        self.current_student_list: [Student] = None

        self.quiz_view.clear_window()

    def show_next_student(self):
        super().show_next_student()

        if self.current_student is None:
            return

        self.current_student_list: [Student] = [self.current_student]
        self.current_student_list.extend(self.students.get_random_student_alternatives(student=self.current_student,
                                                                                       count=2))
        shuffle(self.current_student_list)
        # print(f'Chosen student: {self.current_student.get_full_name()}')
        # print([s.get_full_name() for s in self.current_student_list])

        self.quiz_view.ask_question(student_names=[s.get_full_name() for s in self.current_student_list])

    def chosen_student_name(self, chosen: str):
        # print(f'button {chosen} clicked')
        chosen_student: Student = self.current_student_list[MCController.OPTION[chosen]]
        # print(f'Chosen student = {chosen_student.get_full_name()}')
        # print(f'Shown student  = {self.current_student.get_full_name()}')
        result = chosen_student == self.current_student
        if result:
            self.total_correct_names += 1
        else:
            self.total_wrong_names += 1

        self.quiz_view.show_student_result(result=result,
                                           student_name=self.current_student.get_full_name(),
                                           correct=self.total_correct_names,
                                           wrong=self.total_wrong_names)
