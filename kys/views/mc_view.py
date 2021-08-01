from tkinter import Toplevel, Label, Button, Canvas, StringVar, Frame, ttk


class MCView:
    def __init__(self, master: Toplevel):
        self.master = master
        master.title("KYS - Know Your Students! - Multiple Choice Test")
        master.geometry("800x800")

        self.student_image_canvas = Canvas(master=master, height=400, width=400,
                                           bd=2, bg="grey", relief="ridge")

        self.student_name_A: StringVar = StringVar(master, name='---- A ---')
        self.student_name_B: StringVar = StringVar(master, name='---- B ---')
        self.student_name_C: StringVar = StringVar(master, name='---- C ---')
        self.student_name_A.set('--- A ---')
        self.student_name_B.set('--- B ---')
        self.student_name_C.set('--- C ---')

        self.button_option_A = Button(master=master, textvariable=self.student_name_A, width=50)
        self.button_option_B = Button(master=master, textvariable=self.student_name_B, width=50)
        self.button_option_C = Button(master=master, textvariable=self.student_name_C, width=50)

        self.student_score_frame: Frame = Frame(master)
        self.student_correct_count: StringVar = StringVar(master, name='Correct Count')
        self.student_correct_count.set('0')
        self.student_correct_label = Label(master=self.student_score_frame, text='Correct')
        self.student_correct_count_label = Label(master=self.student_score_frame, textvariable=self.student_correct_count)
        self.student_wrong_count: StringVar = StringVar(master, name='Wrong Count')
        self.student_wrong_count.set('0')
        self.student_wrong_label = Label(master=self.student_score_frame, text='Wrong')
        self.student_wrong_count_label = Label(master=self.student_score_frame, textvariable=self.student_wrong_count)

        self.button_next = Button(master=master, text='Next student', width=50)
        self.button_restart = Button(master=master, text='Start Quiz', width=50)
        self.button_quit = Button(master=master, text='Exit Quiz', width=50, command=self.master.destroy)

        self.score_text: StringVar = StringVar(master, name='Score Label')
        self.score = Label(master=master, textvariable=self.score_text)

        self.student_image_canvas.grid(row=0, column=1)
        self.student_score_frame.grid(row=0, column=2, sticky="N")
        self.student_correct_label.pack()
        self.student_correct_count_label.pack()
        self.student_wrong_label.pack()
        self.student_wrong_count_label.pack()
        self.score.grid(row=2, column=0, columnspan=3)
        self.button_option_A.grid(row=3, column=0, columnspan=3)
        self.button_option_B.grid(row=4, column=0, columnspan=3)
        self.button_option_C.grid(row=5, column=0, columnspan=3)
        self.button_next.grid(row=6, column=0, columnspan=3)
        self.button_restart.grid(row=7, column=0, columnspan=3)
        self.button_quit.grid(row=8, column=0, columnspan=3)

