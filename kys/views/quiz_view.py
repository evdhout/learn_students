from tkinter import Toplevel, Label, Button, Canvas, StringVar, Frame
from PIL import ImageTk
from kys.views.main_view import MainView
from typing import Callable


class QuizView:
    def __init__(self, master_view: MainView, start_command: Callable, next_command: Callable, title: str):
        self.master: Toplevel = Toplevel(master_view.root)
        self.master.title(title)

        self.start_command = start_command
        self.next_command = next_command

        self.quiz_frame = Frame(master=self.master, padx=20, pady=20)

        self.student_image_canvas = Canvas(master=self.quiz_frame, height=400, width=400,
                                           bd=2, bg="grey", relief="ridge")

        self.question_text: StringVar = StringVar(self.master, name='Question text')
        self.question_text.set('Waiting for quiz to start')
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

        self.button_next = Button(master=self.quiz_frame, text='Next student', width=50)

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

    def set_score(self, correct: int = 0, wrong: int = 0):
        self.student_correct_count.set(correct)
        self.student_wrong_count.set(wrong)

    def update_start_button(self, text: str):
        self.button_start.config(text=text)

    def clear_window(self):
        self.question_text.set('--- Waiting to start game ---')
        self.student_image_canvas.delete("all")
        self.unbind_next()

    def show_student_image(self, image: ImageTk):
        self.student_image_canvas.delete('all')
        self.student_image_canvas.config(background='grey')
        self.student_image_canvas.create_image(200, 200, image=image, anchor='center')

    def show_student_result(self, result: bool, student_name: str, correct: int, wrong: int):
        self.student_image_canvas.config(background=f'{"green" if result else "red"}')
        self.question_text.set(f'{"Correct" if result else "WRONG"}! This is {student_name} ')
        self.student_correct_count.set(f'{correct}')
        self.student_wrong_count.set(f'{wrong}')
        self.bind_next()

    def ask_question(self, *args, **kwargs):
        self.question_text.set('Who is this student?')
        self.unbind_next()

    def show_final_score(self, correct: int, wrong: int):
        self.student_image_canvas.delete("all")
        self.unbind_next()

        correct_percentage = round((correct / (correct + wrong)) * 100)
        text_color = "white"
        if correct_percentage < 30:
            self.student_image_canvas.config(background="red")
        elif correct_percentage < 55:
            self.student_image_canvas.config(background="orange")
        elif correct_percentage < 90:
            self.student_image_canvas.config(background="yellow")
            text_color = "black"
        else:
            self.student_image_canvas.config(background="green")

        self.student_image_canvas.create_text(200, 200,
                                              text=f'{correct_percentage}% correct',
                                              font=("Helvetica", 50),
                                              fill=text_color,
                                              anchor='center')
        self.student_image_canvas.create_text(200, 230,
                                              text=f'{correct} / {correct + wrong}',
                                              font=("Helvetica", 25),
                                              fill=text_color,
                                              anchor='center')

    def bind_next(self):
        self.master.bind(sequence='n', func=lambda e: self.next_command())
        self.master.bind(sequence='N', func=lambda e: self.next_command())
        self.button_next.config(command=self.next_command)

    def unbind_next(self):
        self.button_next.config(command=lambda: None)
        self.master.unbind(sequence='n')
        self.master.unbind(sequence='N')
