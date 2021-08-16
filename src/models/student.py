from PIL import ImageTk, Image
from datetime import date
from src.models.gender import Gender


class Student:
    def __init__(self, student_id: str = None, first_name: str = None, last_name: str = None, infix: str = None,
                 date_of_birth: date = None, gender: Gender = Gender(), picture: str = None):
        self.id: str or None = student_id
        self.first_name: str or None = first_name
        self.last_name: str or None = last_name
        self.infix: str or None = infix
        self.date_of_birth: date or None = date_of_birth
        self.gender: Gender or None = gender
        self.picture_path: str or None = picture
        self.image: ImageTk or None = None

    def __str__(self) -> str:
        return (
            f'{self.id}: {self.get_full_name()}\n'
            f'{self.gender} {self.date_of_birth.isoformat()}\n'
            f'{self.picture_path}\n'
        )

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return int(self.id)

    def get_full_name(self) -> str:
        return f'{self.first_name} <{f"{self.infix} " if self.infix else ""}{self.last_name}>'

    def is_female(self) -> bool:
        return self.gender == Gender.FEMALE

    def is_male(self) -> bool:
        return self.gender == Gender.MALE
