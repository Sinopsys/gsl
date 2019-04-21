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
import time

from technologies import OPTIONS
from technologies import LINKS
from utils.log import LOG_CONFIG
from utils.output import print_nested

LOGGING = logging.config.dictConfig(LOG_CONFIG)
__logger__ = logging.getLogger('stdout')


class ChooseError(Exception):
    """
    Error when choosing wrong option
    """
    pass


class Krinkle(object):
    """
    Helps to choose a ledger
    """
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        self.ledger_config = {}

    def load_config(self) -> dict:
        return config.load(self.config_path)

    def prompt(self) -> dict:
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
        print('\n\nThe following config is to be set:\n')
        chosen_to_print = {}
        for k, v in OPTIONS.items():
            chosen_to_print[k] = v[self.ledger_config[k]]
        print_nested(chosen_to_print, 1)
        if input('\nProceed with this config? [YES]/NO:').lower() in ['', 'yes', 'y', 'ye']:
            return chosen_to_print
        else:
            self.prompt()


class Jarquai(object):
    """
    This helps in building corresponding to a selected structure ledger
    ________________________
    ATTENTION, ALPHA VERSION
    Gives links to implemented parts, not uniting them in an actually
    working ledger
    """
    def __init__(self, options):
        self.selected_options = options

    def build_ledger(self):
        return self.match_links()

    def match_links(self):
        res = {}
        for k, v in self.selected_options.items():
            res[v] = LINKS[v]
        print_nested(res, 1)


def main() -> None:
    __logger__.info('Start Goodsteel Ledger: a program for generating distributed ledgers')
    config_path = 'config.yaml'
    kr = Krinkle(config_path)
    options = kr.prompt()
    __logger__.info('Start getting your ledger\'s algorithms')
    time.sleep(2)
    jq = Jarquai(options)
    jq.build_ledger()


if __name__ == '__main__':
    main()

