#!python3
from kys.models.configuration import Configuration
from kys.models.students import Students
from kys.controllers.main_controller import MainController


if __name__ == '__main__':
    print('Running KYS - Know Your Students')
    config = Configuration()
    print(config)

    students = Students()

    main = MainController(students=students, config=config)
