from tkinter import Toplevel, Label, Button, Canvas, StringVar, Frame, NORMAL, DISABLED
from PIL import ImageTk
from kys.views.main_view import MainView
from typing import Callable


class MCView:
    def __init__(self, master_view: MainView,
                 start_command: Callable,
                 next_command: Callable,
                 choice_button_command: Callable):
        self.master: Toplevel = Toplevel(master_view.root)
        self.master.title("KYS - Know Your Students! - Multiple Choice Test")
        self.master.geometry("800x800")

        self.start_command = start_command
        self.next_command = next_command
        self.choice_button_command = choice_button_command

        self.student_image_canvas = Canvas(master=self.master, height=400, width=400,
                                           bd=2, bg="grey", relief="ridge")

        # prepare the buttons
        self.student_name_buttons: {str: Button} = {}

        for key in ['A', 'B', 'C']:
            self.student_name_buttons[key] = Button(master=self.master, text=f'--- {key} ---', width=50,
                                                    command=lambda k=key: choice_button_command(chosen=k))

        # prepare the scoreboard
        self.student_score_frame: Frame = Frame(self.master)
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

        # prepare the quiz buttons
        self.button_next = Button(master=self.master, text='Next student', width=50, command=next_command)

        self.button_frame = Frame(self.master)
        self.button_start = Button(master=self.button_frame, text='Start Quiz', width=10, command=start_command)
        self.button_quit = Button(master=self.button_frame, text='Exit Quiz', width=10, command=self.master.destroy)

        # prepare the final score
        self.score_text: StringVar = StringVar(self.master, name='Score Label')
        self.score = Label(master=self.master, textvariable=self.score_text)

        # place everything on the grid
        self.student_image_canvas.grid(row=0, column=1, rowspan=2)
        self.student_score_frame.grid(row=0, column=2, sticky="N")
        self.student_correct_label.pack()
        self.student_correct_count_label.pack()
        self.student_wrong_label.pack()
        self.student_wrong_count_label.pack()
        self.score.grid(row=2, column=1)
        Label(master=self.master, text='A:').grid(row=3, column=0, sticky="E")
        Label(master=self.master, text='B:').grid(row=4, column=0, sticky="E")
        Label(master=self.master, text='C:').grid(row=5, column=0, sticky="E")
        self.student_name_buttons['A'].grid(row=3, column=1)
        self.student_name_buttons['B'].grid(row=4, column=1)
        self.student_name_buttons['C'].grid(row=5, column=1)
        self.button_next.grid(row=6, column=1)
        self.button_frame.grid(row=1, column=2, sticky="S")
        self.button_start.pack()
        self.button_quit.pack()

    def clear_window(self):
        for key, student_name_button in self.student_name_buttons.items():
            student_name_button.config(text=f'--- {key} ---')

        self.score_text.set('--- Waiting to start game ---')

        self.set_button_state(name_button_state=DISABLED, next_button_state=DISABLED)

        self.student_image_canvas.delete("all")

    def set_button_state(self,
                         name_button_state=DISABLED,
                         next_button_state=DISABLED):
        for key, button in self.student_name_buttons.items():
            if name_button_state == DISABLED:
                button.config(command=lambda: None)
            else:
                button.config(command=lambda k=key: self.choice_button_command(k))
        if name_button_state == DISABLED:
            self.unbind_option_keys()
        else:
            self.bind_option_keys()

        if next_button_state == DISABLED:
            self.button_next.config(command=lambda: None)
            self.unbind_next_key()
        else:
            self.button_next.config(command=self.next_command)
            self.bind_next_key()

    def bind_option_keys(self):
        for key in self.student_name_buttons:
            self.master.bind(sequence=key, func=lambda e, k=key: self.choice_button_command(chosen=k))
            self.master.bind(sequence=key.lower(), func=lambda e, k=key: self.choice_button_command(chosen=k))

    def unbind_option_keys(self):
        for key in self.student_name_buttons:
            self.master.unbind(sequence=key)
            self.master.unbind(sequence=key.lower())

    def bind_next_key(self):
        self.master.bind(sequence='n', func=lambda e: self.next_command())
        self.master.bind(sequence='N', func=lambda e: self.next_command())

    def unbind_next_key(self):
        self.master.unbind(sequence='n')
        self.master.unbind(sequence='N')

    def set_score(self, correct: int = 0, wrong: int = 0):
        self.student_correct_count.set(correct)
        self.student_wrong_count.set(wrong)

    def update_start_button(self, text: str):
        self.button_start.config(text=text)

    def show_student_image(self, image: ImageTk):
        self.student_image_canvas.delete('all')
        self.student_image_canvas.config(background='grey')
        self.student_image_canvas.create_image(200, 200, image=image, anchor='center')

    def show_student_result(self, result: bool, student_name: str, correct: int, wrong: int):
        self.set_button_state(name_button_state=DISABLED, next_button_state=NORMAL)
        self.student_image_canvas.config(background=f'{"green" if result else "red"}')
        self.score_text.set(f'{"Correct" if result else "WRONG"}! This is {student_name} ')
        self.student_correct_count.set(f'{correct}')
        self.student_wrong_count.set(f'{wrong}')

    def set_student_names(self, student_names: [str]):
        for key, student_name_button in self.student_name_buttons.items():
            student_name_button.config(text=student_names.pop(0))

    def ask_question(self, student_names: [str]):
        self.set_student_names(student_names=student_names)
        self.set_button_state(name_button_state=NORMAL, next_button_state=DISABLED)
        self.score_text.set('Who is this student?')

    def show_final_score(self, correct: int, wrong: int):
        self.student_image_canvas.delete("all")

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
