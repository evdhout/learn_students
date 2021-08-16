#!python3
import os
import gettext
from pathlib import Path
from kys.models.configuration import Configuration
from kys.controllers.main_controller import MainController

if __name__ == '__main__':
    print(Path(__file__).parent)
    config = Configuration(base_path=Path(__file__).parent)

    try:
        os.environ['LANGUAGE'] = config.kys['language']
    except KeyError:
        os.environ['LANGUAGE'] = 'en_EN'

    gettext.install('kys', 'locales')

    main = MainController(config=config)
