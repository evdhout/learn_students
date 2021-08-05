#!python3
import gettext
from kys.models.configuration import Configuration
from kys.models.students import Students
from kys.controllers.main_controller import MainController


if __name__ == '__main__':
    print(_('Running KYS - Know Your Students'))
    config = Configuration()
    print(config)
    translations = gettext.translation('kys', localedir='locales', languages=config.language['language'])
    translations.install()
    _ = translations.gettext
    ngettext = translations.ngettext

    students = Students()

    main = MainController(students=students, config=config)
