from tkinter import Toplevel, Label, Button, Canvas, StringVar, Frame, NORMAL, DISABLED
from PIL import ImageTk
from kys.views.main_view import MainView
from typing import Callable


class QuizView:
    def __init__(self, master_view: MainView, start_command: Callable, next_command: Callable, title: str):
        self.master: Toplevel = Toplevel(master_view.root)
        self.master.title = title

        self.start_command = start_command
        self.next_command = next_command

        self.quiz_frame = Frame(master=self.master, padx=20, pady=20)

        self.student_image_canvas = Canvas(master=self.quiz_frame, height=400, width=400,
                                           bd=2, bg="grey", relief="ridge")

        self.question_text: StringVar = StringVar(self.master, name='Question text')
        self.question = Label(master=self.quiz_frame, textvariable=self.question_text)

        # the scoreboard
        self.student_score_frame: Frame = Frame(self.quiz_frame)
        self.student_correct_count: StringVar = StringVar(self.master, name='Correct Count')
        self.student_correct_count.set('0')
        self.student_correct_label = Label(master=self.student_score_frame, text='Correct')
        self.student_correct_count_label = Label(master=self.student_score_frame,
                                                 textvariable=self.student_correct_count)
        self.student_wrong_count: StringVar = StringVar(self.master, name='Wrong Count')
        self.student_wrong_count.set('0')
        self.student_wrong_label = Label(master=self.student_score_frame, text='Wrong')
        self.student_wrong_count_label = Label(master=self.student_score_frame,
                                               textvariable=self.student_wrong_count)

        self.button_frame = Frame(self.quiz_frame)
        self.button_start = Button(master=self.button_frame, text='Start Quiz', width=10, command=start_command)
        self.button_quit = Button(master=self.button_frame, text='Exit Quiz', width=10, command=self.master.destroy)

        self.button_next = Button(master=self.quiz_frame, text='Next student', width=50, command=next_command)

        self.quiz_frame.grid(row=0, column=0)
        self.student_image_canvas.grid(row=0, column=1, rowspan=2)
        self.student_score_frame.grid(row=0, column=2, sticky="N")
        self.student_correct_label.pack()
        self.student_correct_count_label.pack()
        self.student_wrong_label.pack()
        self.student_wrong_count_label.pack()

        self.question.grid(row=2, column=1)

        self.button_next.grid(row=6, column=1)

        self.button_frame.grid(row=1, column=2, sticky="S")
        self.button_start.pack()
        self.button_quit.pack()
