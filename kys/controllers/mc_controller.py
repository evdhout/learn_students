from enum import Enum
from random import shuffle

from kys.models.student import Student
from kys.models.students import Students
from kys.views.mc_view import MCView
from kys.views.main_view import MainView


class ButtonStyle(Enum):
    NORMAL = "normal"
    CORRECT = "correct"
    WRONG = "wrong"


class MCController:
    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_C = 2

    OPTION = {'A': 0, 'B': 1, 'C': 2, 'D': 4}

    def __init__(self, master: MainView, students: Students):

        self.students: Students = students
        self.master: MainView = master

        self.mc_view: MCView = MCView(self.master,
                                      start_command=self.start_quiz,
                                      next_command=self.show_next_student,
                                      choice_button_command=self.chosen_student_name)

        self.total_correct_names: int = 0
        self.total_wrong_names: int = 0
        self.total_students: int = len(self.students)
        self.students_iterator = None

        self.current_student: Student or None = None
        self.current_student_list: [Student] = None

        self.mc_view.clear_window()

    def start_quiz(self):
        self.total_correct_names = 0
        self.total_wrong_names = 0
        self.mc_view.set_score()
        self.students_iterator = iter(self.students)
        self.show_next_student()
        self.mc_view.update_start_button(text='Restart Quiz')

    def show_next_student(self):
        try:
            self.current_student = next(self.students_iterator)
        except StopIteration:
            self.end_of_quiz()
            return

        # print('Attempting to display:')
        # print(self.current_student)
        self.mc_view.show_student_image(image=self.current_student.image)

        self.current_student_list: [Student] = [self.current_student]
        self.current_student_list.extend(self.students.get_random_student_alternatives(student=self.current_student,
                                                                                       count=2))
        shuffle(self.current_student_list)
        print(f'Chosen student: {self.current_student.get_full_name()}')
        print([s.get_full_name() for s in self.current_student_list])

        self.mc_view.ask_question(student_names=[s.get_full_name() for s in self.current_student_list])

    def chosen_student_name(self, chosen: str):
        print(f'button {chosen} clicked')
        chosen_student: Student = self.current_student_list[MCController.OPTION[chosen]]
        print(f'Chosen student = {chosen_student.get_full_name()}')
        print(f'Shown student  = {self.current_student.get_full_name()}')
        result = chosen_student == self.current_student
        if result:
            self.total_correct_names += 1
        else:
            self.total_wrong_names += 1

        self.mc_view.show_student_result(result=result,
                                         student_name=self.current_student.get_full_name(),
                                         correct=self.total_correct_names,
                                         wrong=self.total_wrong_names)

    def end_of_quiz(self):
        self.mc_view.show_final_score(correct=self.total_correct_names, wrong=self.total_wrong_names)
