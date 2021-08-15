#!python3
from kys.models.configuration import Configuration
from kys.controllers.main_controller import MainController
import os
import gettext

if __name__ == '__main__':
    config = Configuration()

    try:
        os.environ['LANGUAGE'] = config.kys['language']
    except KeyError:
        os.environ['LANGUAGE'] = 'en_EN'

    gettext.install('kys', 'locales')

    main = MainController(config=config)
