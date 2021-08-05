from typing import Callable
from tkinter import StringVar, Entry

from kys.views.main_view import MainView
from kys.views.quiz_view import QuizView


class TypeView(QuizView):
    def __init__(self, master_view: MainView,
                 start_command: Callable,
                 next_command: Callable,
                 enter_command: Callable):
        super().__init__(master_view=master_view,
                         start_command=start_command,
                         next_command=next_command,
                         title=_('KYS - Know Your Students! - Typing Test'))
        self.enter_command: Callable = enter_command

        self.name_entry_value = StringVar(master=self.master, name='Name Entry Value')
        self.name_entry = Entry(master=self.quiz_frame, textvariable=self.name_entry_value, width=50)
        self.name_entry.grid(row=3, column=1)

    def bind_enter(self, command: Callable):
        self.master.bind(sequence='<Return>', func=lambda e: command())

    def unbind_enter(self):
        self.master.unbind(sequence='<Return>')

    def get_name_entry_value(self):
        return self.name_entry_value.get()

    def ask_question(self, *args, **kwargs):
        super().ask_question()
        self.name_entry_value.set('')
        self.name_entry.focus_set()
        self.bind_enter(command=self.enter_command)

    def show_student_result(self, result: bool, student_name: str, correct: int, wrong: int):
        super().show_student_result(result=result, student_name=student_name, correct=correct, wrong=wrong)
        self.bind_enter(command=self.next_command)
