#!python3
from kys.models.configuration import Configuration
from kys.models.students import Students
from kys.controllers.main_controller import MainController
import os
import gettext

if __name__ == '__main__':
    print('Running KYS - Know Your Students')
    config = Configuration()
    print(config)

    try:
        os.environ['LANGUAGE'] = config.language['language']
    except KeyError:
        os.environ['LANGUAGE'] = 'en_EN'

    print(os.environ['LANGUAGE'])
    gettext.install('kys', 'locales')

    students = Students()

    main = MainController(students=students, config=config)
