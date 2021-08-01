from enum import Enum
from random import shuffle
from tkinter import Toplevel, Button, DISABLED, NORMAL

from kys.models.student import Student
from kys.models.students import Students
from kys.views.mc_view import MCView


class ButtonStyle(Enum):
    NORMAL = "normal"
    CORRECT = "correct"
    WRONG = "wrong"


class MCController:
    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_C = 2

    def __init__(self, master: Toplevel, students: Students):
        self.students = students
        self.master = master

        self.window: MCView = MCView(self.master)

        self.total_correct_names: int = 0
        self.total_wrong_names: int = 0
        self.total_students: int = len(self.students)
        self.students_iterator = None

        self.current_student: Student or None = None
        self.current_student_list: [Student] = None

        self.window.button_restart.config(command=self.play_game)
        self.window.button_next.config(command=self.show_next_student)

        self.window.button_option_A.config(command=lambda: self.mc_button_clicked(option=MCController.BUTTON_A))
        self.window.button_option_B.config(command=lambda: self.mc_button_clicked(option=MCController.BUTTON_B))
        self.window.button_option_C.config(command=lambda: self.mc_button_clicked(option=MCController.BUTTON_C))

        self.button_options_list: [Button] = [
            self.window.button_option_A,
            self.window.button_option_B,
            self.window.button_option_C
        ]

        self.clear_window()

    def clear_window(self):
        self.window.student_name_A.set('--- A ---')
        self.window.student_name_B.set('--- B ---')
        self.window.student_name_C.set('--- C ---')
        self.window.score_text.set('--- Waiting to start game ---')
        self.set_button_state(name_button_state=DISABLED, next_button_state=DISABLED)

        self.window.student_image_canvas.delete("all")

    def set_button_state(self,
                         name_button_state=DISABLED,
                         next_button_state=DISABLED):
        for button in self.button_options_list:
            button.config(state=name_button_state)

        self.window.button_next.config(state=next_button_state)

    def play_game(self):
        self.total_correct_names = 0
        self.total_wrong_names = 0
        self.window.student_correct_count.set(f'{self.total_correct_names}')
        self.window.student_wrong_count.set(f'{self.total_wrong_names}')
        self.students_iterator = iter(self.students)
        self.show_next_student()
        self.window.button_restart.config(text='Restart Quiz')

    def show_next_student(self):
        try:
            self.current_student = next(self.students_iterator)
        except StopIteration:
            self.game_over()
            return

        print('Attempting to display:')
        print(self.current_student)

        self.window.student_image_canvas.delete('all')
        self.window.student_image_canvas.config(background='grey')
        self.window.student_image_canvas.create_image(200, 200, image=self.current_student.image, anchor='center')

        self.current_student_list: [Student] = [self.current_student]
        self.current_student_list.extend(self.students.get_random_students(student=self.current_student, count=2))
        shuffle(self.current_student_list)
        print(self.current_student_list)

        self.window.student_name_A.set(self.current_student_list[0].get_full_name())
        self.window.student_name_B.set(self.current_student_list[1].get_full_name())
        self.window.student_name_C.set(self.current_student_list[2].get_full_name())
        self.window.score_text.set('Who is this student?')

        self.set_button_state(name_button_state=NORMAL, next_button_state=DISABLED)

    def mc_button_clicked(self, option: int):
        print(f'button {option} clicked')
        result = ''
        if self.current_student_list[option] == self.current_student:
            self.total_correct_names += 1
            result = f'Correct'
            self.window.student_image_canvas.config(background="green")
        else:
            self.total_wrong_names += 1
            result = f'WRONG'
            self.window.student_image_canvas.config(background="red")

        self.set_button_state(name_button_state=DISABLED, next_button_state=NORMAL)
        self.window.score_text.set(f'{result}! This is {self.current_student.get_full_name()} ')
        self.window.student_correct_count.set(f'{self.total_correct_names}')
        self.window.student_wrong_count.set(f'{self.total_wrong_names}')

    def game_over(self):
        self.clear_window()
        correct_percentage = self._get_correct_percentage()
        print(correct_percentage)
        if correct_percentage < 30:
            self.window.student_image_canvas.config(background="red")
        elif correct_percentage < 55:
            self.window.student_image_canvas.config(background="orange")
        elif correct_percentage < 90:
            self.window.student_image_canvas.config(background="yellow")
        else:
            self.window.student_image_canvas.config(background="green")

        self.window.student_image_canvas.create_text(200, 200,
                                                     text=f'{self._get_correct_vs_total_string()}\n'
                                                          f'{self._get_correct_percentage_string()} correct',
                                                     font=("Helvetica", 50),
                                                     anchor='center')

    def _get_correct_vs_total_string(self):
        return f'{self.total_correct_names} / {self.total_students}'

    def _get_correct_percentage_string(self):
        return f'{self._get_correct_percentage()}%'

    def _get_correct_percentage(self) -> int:
        return int(round(self.total_correct_names / self.total_students * 100))
