import gettext
import random
from collections import deque
from src.models.student import Student
from src.models.gender import Gender


class Students:
    def __init__(self):
        self.students: {str: Student} = {}
        self.female_students: [Student] = []
        self.male_students: [Student] = []
        self.student_queue: [Student] = deque()

    def __len__(self) -> int:
        return len(self.students)

    def __str__(self) -> str:
        student_count = len(self.students)
        return gettext.ngettext('{n} student registered', '{n} students registered',
                                student_count).format(n=student_count)
        # if 0 == student_count:
        #     return ('No students registered')
        # elif 1 == student_count:
        #     return '1 student registered'
        # else:
        #     return f'{student_count} students registered'

    def __iter__(self):
        self.student_queue = deque([*self.students])
        random.shuffle(self.student_queue)
        return self

    def __next__(self) -> Student:
        try:
            return self.students[self.student_queue.pop()]
        except IndexError:
            raise StopIteration

    def add_student(self, student: Student):
        self.students[student.id] = student
        if not student.gender == Gender.FEMALE:
            self.male_students.append(student)
        if not student.gender == Gender.MALE:
            self.female_students.append(student)

    def get_student(self, student_id: str) -> Student or None:
        try:
            return self.students[student_id]
        except KeyError:
            print(f'student id {student_id} not found')
            return None

    def get_random_student_alternatives(self, student: Student, count: int = 4):
        pick_list: [Student]
        if student.is_female():
            pick_list = self.female_students
        else:
            pick_list = self.male_students
        return random.sample([s for s in pick_list if not s == student], count)
