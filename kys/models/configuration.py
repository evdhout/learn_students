import configparser
import argparse
import os


class Configuration:
    def __init__(self):
        self.path: {str: str} = {}
        self.csv: {str: str} = {}
        self.gender: {str: str} = {}
        self.picture: {str: str} = {}
        self.kys: {str: str} = {}
        self.config_read = False
        self.config_file = ''

        parser = argparse.ArgumentParser(description='Know Your Students (KYS): train student names from pictures')
        parser.add_argument('-c', '--config', type=self._arg_file_exists, default='data/config.ini',
                            help='Path to configuration file')
        args = parser.parse_args()

        try:
            self.parse_ini(ini=self.file_exists(args.config))
        except FileNotFoundError:
            return

    def parse_ini(self, ini: str):
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(ini)
        self.path: {str: str} = {n: v for n, v in config.items('Path')}
        self.csv: {str: str} = {n: v for n, v in config.items('CSV')}
        self.gender: {str: str} = {n: v for n, v in config.items('Gender')}
        self.picture: {str: str} = {n: v for n, v in config.items('Picture')}
        self.kys: {str: str} = {n: v for n, v in config.items('KYS')}
        self.config_read = True
        self.config_file = ini

    def __str__(self):
        return(f'Path: {self.path}\n'
               f'CSV: {self.csv}\n'
               f'Picture: {self.picture}\n'
               f'Gender: {self.gender}\n')

    def _arg_path_exists(self, pathname: str) -> str:
        try:
            return self.path_exists(pathname)
        except NotADirectoryError as e:
            raise argparse.ArgumentTypeError(e)

    @staticmethod
    def path_exists(pathname: str) -> str:
        if os.path.isdir(os.path.expanduser(pathname)):
            return os.path.expanduser(pathname)
        else:
            raise NotADirectoryError(_('{} is not a valid path').format(pathname))

    def _arg_file_exists(self, filename: str) -> str:
        try:
            return self.file_exists(filename)
        except FileNotFoundError as e:
            raise argparse.ArgumentTypeError(e)

    @staticmethod
    def file_exists(filename: str) -> str:
        if os.path.isfile(os.path.expanduser(filename)):
            return os.path.expanduser(filename)
        else:
            raise FileNotFoundError(_('{} is not a valid file').format(filename))
