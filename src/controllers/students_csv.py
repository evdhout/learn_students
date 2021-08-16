import csv
import datetime
from pathlib import Path

from src.models.configuration import Configuration
from src.models.gender import Gender
from src.models.student import Student
from src.models.students import Students


class StudentsCSV:
    def __init__(self, students: Students, config: Configuration):
        self.students: Students = students
        self.config: Configuration = config
        self._read_csv()

    def get_resource_path(self, path: str):
        full_path = Path(path).expanduser()
        if not full_path.is_absolute():
            full_path = self.config.group_path / full_path
        return str(full_path)

    def _read_csv(self):
        student_csv = self.get_resource_path(self.config.csv["student_csv"])

        with open(student_csv) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.config.csv['delimiter'])

            infix_present: bool = self.config.csv['infix'] in reader.fieldnames
            for row in reader:
                self.students.add_student(
                    Student(student_id=row[self.config.csv['student_id']],
                            first_name=row[self.config.csv['first_name']],
                            last_name=row[self.config.csv['last_name']],
                            infix=row[self.config.csv['infix']] if infix_present else '',
                            gender=self._get_gender(row[self.config.csv['gender']]),
                            date_of_birth=datetime.datetime.strptime(
                                row[self.config.csv['date_of_birth']],
                                self.config.csv['date_of_birth_format']).date(),
                            picture=self._create_student_image_filename(row[self.config.csv['student_id']])
                            )
                )

    def _create_student_image_filename(self, student_id: str) -> str:
        return self.get_resource_path((
            f"{self.config.group_path}/"
            f"{self.config.picture['prefix']}{student_id}{self.config.picture['suffix']}"
            f".{self.config.picture['extension']}"
            ))

    def _get_gender(self, gender: str) -> Gender:
        if gender == self.config.gender['female']:
            return Gender(Gender.FEMALE)
        elif gender == self.config.gender['male']:
            return Gender(Gender.MALE)
        else:
            return Gender(Gender.NEUTRAL)
