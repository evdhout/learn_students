from pathlib import Path
import configparser
import argparse


class Configuration:
    def __init__(self, app_path: Path = None):
        self.app_path: Path = app_path
        self.group_path: Path or None = None
        self.path: {str: str} = {}
        self.csv: {str: str} = {}
        self.gender: {str: str} = {}
        self.picture: {str: str} = {}
        self.kys: {str: str} = {}

        parser = argparse.ArgumentParser(description='Know Your Students (KYS): train student names from pictures')
        parser.add_argument('-c', '--config', type=self._arg_file_resource, default='data/config.ini',
                            help='Path to configuration file')
        try:
            args = parser.parse_args()
            self.parse_ini(ini=args.config)
        except argparse.ArgumentTypeError:
            pass

    def parse_ini(self, ini: str):
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        ini_file = Path(self.get_resource_path(ini))
        config.read(ini_file)
        self.csv: {str: str} = {n: v for n, v in config.items('CSV')}
        self.gender: {str: str} = {n: v for n, v in config.items('Gender')}
        self.picture: {str: str} = {n: v for n, v in config.items('Picture')}
        self.kys: {str: str} = {n: v for n, v in config.items('KYS')}

        self.group_path = Path(self.kys.get('group_path', ini_file.parent))
        if not self.group_path.is_absolute():
            self.group_path = ini_file.parent / self.group_path

    def __str__(self):
        return(f'Path: {self.path}\n'
               f'CSV: {self.csv}\n'
               f'Picture: {self.picture}\n'
               f'Gender: {self.gender}\n')

    def _arg_path_resource(self, pathname: str) -> str:
        path = self.get_resource_path(pathname)
        if not self.path_exists(path):
            raise argparse.ArgumentTypeError(_('{} is not a valid path').format(pathname))
        return str(path)

    def _arg_file_resource(self, filename: str) -> str:
        file = self.get_resource_path(filename)
        if not self.file_exists(file):
            raise argparse.ArgumentTypeError(_('{} is not a valid file').format(filename))
        return str(file)

    @staticmethod
    def file_exists(filename: str) -> bool:
        return Path(filename).is_file()

    @staticmethod
    def path_exists(pathname: str) -> bool:
        return Path(pathname).is_dir()

    def get_resource_path(self, path: str) -> str:
        # print(f'GRP path = {path}')
        resource_path = Path(path).expanduser()
        # print(f'GRP resource path = {resource_path}')
        if not resource_path.is_absolute():
            resource_path = self.app_path / resource_path
            # print(f'GRP absolute resource path = {resource_path}')
        return str(resource_path)

    def is_config_read(self) -> bool:
        return bool(self.kys)
