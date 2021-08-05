from tkinter import Label, Button
from typing import Callable

from kys.views.main_view import MainView
from kys.views.quiz_view import QuizView


class MCView(QuizView):
    def __init__(self, master_view: MainView,
                 start_command: Callable,
                 next_command: Callable,
                 choice_button_command: Callable):
        super().__init__(master_view=master_view,
                         start_command=start_command,
                         next_command=next_command,
                         title=_("KYS - Know Your Students! - Multiple Choice Test"))

        self.choice_button_command = choice_button_command

        # prepare the buttons
        self.student_name_buttons: {str: Button} = {}
        for key in ['A', 'B', 'C']:
            self.student_name_buttons[key] = Button(master=self.quiz_frame, text=f'--- {key} ---', width=50,
                                                    command=lambda k=key: choice_button_command(chosen=k))

        # place everything on the grid
        self.student_image_canvas.grid(row=0, column=1, rowspan=2)
        self.student_score_frame.grid(row=0, column=2, sticky="N")
        self.student_correct_label.pack()
        self.student_correct_count_label.pack()
        self.student_wrong_label.pack()
        self.student_wrong_count_label.pack()
        self.question.grid(row=2, column=1)
        Label(master=self.quiz_frame, text='A:').grid(row=3, column=0, sticky="E")
        Label(master=self.quiz_frame, text='B:').grid(row=4, column=0, sticky="E")
        Label(master=self.quiz_frame, text='C:').grid(row=5, column=0, sticky="E")
        self.student_name_buttons['A'].grid(row=3, column=1)
        self.student_name_buttons['B'].grid(row=4, column=1)
        self.student_name_buttons['C'].grid(row=5, column=1)
        self.button_next.grid(row=6, column=1)
        self.button_frame.grid(row=1, column=2, sticky="S")
        self.button_start.pack()
        self.button_quit.pack()

    def clear_window(self):
        super().clear_window()
        for key, student_name_button in self.student_name_buttons.items():
            student_name_button.config(text=f'--- {key} ---')
        self.unbind_options()

    def bind_options(self):
        for key, button in self.student_name_buttons.items():
            self.master.bind(sequence=key, func=lambda e, k=key: self.choice_button_command(chosen=k))
            self.master.bind(sequence=key.lower(), func=lambda e, k=key: self.choice_button_command(chosen=k))
            button.config(command=lambda k=key: self.choice_button_command(k))

    def unbind_options(self):
        for key, button in self.student_name_buttons.items():
            self.master.unbind(sequence=key)
            self.master.unbind(sequence=key.lower())
            button.config(command=lambda: None)

    def show_student_result(self, result: bool, student_name: str, correct: int, wrong: int):
        super().show_student_result(result=result, student_name=student_name, correct=correct, wrong=wrong)
        self.unbind_options()

    def set_student_names(self, student_names: [str]):
        for key, student_name_button in self.student_name_buttons.items():
            student_name_button.config(text=student_names.pop(0))

    def ask_question(self, student_names: [str], *args, **kwargs):
        super().ask_question()
        self.set_student_names(student_names=student_names)
        self.bind_options()

    def show_final_score(self, correct: int, wrong: int):
        super().show_final_score(correct=correct, wrong=wrong)
        self.unbind_options()
