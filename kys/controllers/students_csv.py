import csv
import datetime

from kys.models.configuration import Configuration
from kys.models.gender import Gender
from kys.models.student import Student
from kys.models.students import Students


class StudentsCSV:
    def __init__(self, students: Students, config: Configuration):
        self.students: Students = students
        self.config: Configuration = config

        self._read_csv()

    def _read_csv(self):
        student_csv = Configuration.file_exists(self.config.csv["student_csv"])

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
                            picture=self._create_filename(row[self.config.csv['student_id']])
                            )
                )

    def _create_filename(self, student_id: str) -> str:
        return Configuration.file_exists((f"{self.config.path['group_path']}/{self.config.picture['prefix']}"
                                          f"{student_id}{self.config.picture['suffix']}"
                                          f".{self.config.picture['extension']}"
                                          ))

    def _get_gender(self, gender: str) -> Gender:
        if gender == self.config.gender['female']:
            return Gender(Gender.FEMALE)
        elif gender == self.config.gender['male']:
            return Gender(Gender.MALE)
        else:
            return Gender(Gender.NEUTRAL)
