from kys.views.main_view import MainView
from kys.models.students import Students
from kys.models.student import Student
from kys.views.quiz_view import QuizView


class QuizController:
    def __init__(self, master: MainView, students: Students):
        self.students: Students = students
        self.master: MainView = master

        self.total_correct_names: int = 0
        self.total_wrong_names: int = 0
        self.total_students: int = len(self.students)
        self.students_iterator = None

        self.quiz_view: QuizView or None = None

        self.current_student: Student or None = None

    def start_quiz(self):
        self.total_correct_names = 0
        self.total_wrong_names = 0
        self.quiz_view.set_score()
        self.students_iterator = iter(self.students)
        self.show_next_student()
        self.quiz_view.update_start_button(text='Restart Quiz')

    def show_next_student(self):
        try:
            self.current_student = next(self.students_iterator)
        except StopIteration:
            self.current_student = None
            self.end_of_quiz()
            return

        self.quiz_view.show_student_image(image=self.current_student.image)

    def end_of_quiz(self):
        self.quiz_view.show_final_score(correct=self.total_correct_names, wrong=self.total_wrong_names)


