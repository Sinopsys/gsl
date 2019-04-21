"""
    gsl -- Goodsteel ledger. A program for building an own distributed ledger

    Copyright (C) 2019  Kirill Kupriyanov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
"""
    Module for working with config
"""
import os
import yaml
import logging.config

from utils.log import LOG_CONFIG

LOGGING = logging.config.dictConfig(LOG_CONFIG)
__logger__ = logging.getLogger('stdout')


# Define Exceptions
class LoadConfigError(Exception):
    """
        Common config exception
    """
    pass


class ConfigYamlError(LoadConfigError):
    """
        Yaml parse config exception
    """
    pass


class CongifValidateError(LoadConfigError):
    """
        Config validation exception
    """
    pass


def load(path: str) -> dict:
    """
    Load and parse config file
    : param path : str
        Path to a config file
    : return : dict
        Loaded and parsed config
    """
    __logger__.info(f'Loading config from {path}')
    config = _read_(path)
    if not config:
        raise ConfigYamlError('Load configuration form yaml Fail')
    __logger__.info('Configuration loaded')
    return config


def _read_(path: str) -> dict:
    """
    Reads config from path
    : param path : str
        Path to a config file
    : return : dict
        Read yaml config
    """
    config = {}
    if not os.path.exists(path):
        raise OSError(f'No such file or directory {path}, please check if file\
                exists')

    with open(path, 'r') as __fd__:
        try:
            config = yaml.load(__fd__, Loader=yaml.BaseLoader)
        except yaml.YAMLError as err:
            __logger__.exception(
                f'Error {err.__class__.__name__} occurred when parse yaml\
                parse config file, {err}'
            )
        except Exception as err:
            __logger__.exception(
                f'Unknown error {err.__class__.__name__} occurred when parse\
                yaml parse config file, {err}'
            )

    return config

