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
    Init script for creating ledger.
"""
import sys
import os
import yaml
import logging.config
import config

from technologies import OPTIONS
from utils.log import LOG_CONFIG
from utils.output import print_nested

LOGGING = logging.config.dictConfig(LOG_CONFIG)
__logger__ = logging.getLogger('stdout')


class Krinkle(object):
    """
    Helps to choose a ledger
    """
    pass


class ChooseError(Exception):
    """
    Error when choosing wrong option
    """
    pass


class Jarquai(object):
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        self.ledger_config = {}

    def load_config(self) -> dict:
        return config.load(self.config_path)

    def prompt(self):
        for k, v in OPTIONS.items():
            print(f'\nChoose type of {k} of the ledger')
            if isinstance(v, list):
                for num, opt in enumerate(v):
                    print(f'{num+1}: {opt}', end='\n')
                try:
                    n = input(f'Enter num from 1 to {len(v)}, default [1]: ')
                    n = 0 if n == '' else int(n) - 1
                    if n < 0 or n >= len(v):
                        raise ChooseError
                    self.ledger_config[k] = n
                except Exception as e:
                    __logger__.exception(str(e))
                    return
            else:
                print(v)
        print('\n\nThe following config is to be set:')
        for k, v in OPTIONS.items():
            print(f'{k}: {v[self.ledger_config[k]]}')
        if input('\nProceed with this config? [YES]/NO:').lower() in ['', 'yes', 'y', 'ye']:
            return
        else:
            self.prompt()


def main() -> None:
    __logger__.info('Start Goodsteel Ledger: a program for generating distributed ledgers')
    config_path = 'config.yaml'
    jq = Jarquai(config_path)
    jq.prompt()


if __name__ == '__main__':
    main()

