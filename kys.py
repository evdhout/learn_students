#!python3
import os
import gettext
from pathlib import Path
from src.models.configuration import Configuration
from src.controllers.main_controller import MainController

if __name__ == '__main__':
    config = Configuration(app_path=Path(__file__).parent)

    try:
        os.environ['LANGUAGE'] = config.kys['language']
    except KeyError:
        os.environ['LANGUAGE'] = 'en_EN'

    gettext.install('kys', 'locales')

    main = MainController(config=config)
