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
import time
import argparse
import yaml
import logging.config

import config
from prolific_writer import ProlificWriter
from technologies import OPTIONS
from technologies import LINKS
from utils.log import LOG_CONFIG
from utils.misc import get_version
from utils.output import print_nested


DEFAULT_CONFIG_PATH = '/etc/gsl/config.yaml'
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
        """
        : param config_path : str
            Path to a config file
        """
        self.config_path = config_path
        self.config = self.load_config()
        self.ledger_config = {}

    def load_config(self) -> dict:
        """
        Load and parse config file
        : return : dict
            Loaded and parsed config
        """
        return config.load(self.config_path)

    def print_description(self, name, path):
        print(f'''
                =============================================
                ==============INITIALISE LEDGER==============
                =============================================

                Name: {name}
                Path: {path}

                =============================================
                ==============MAKE YOUR CHOISES==============
                =============================================
               '''.format(name=name, path=path))

    def prompt(self, name, path) -> dict:
        """
        Prompts user to choose algorithms that will be used in a ledger
        : returns : dict
            Chosen options
            Example:
                 structure:
                     - Blockchain
                 openess:
                     - Public
                 consensus:
                     - PoW
                 hashing:
                     - SHA-256
                 random:
                     - DRBG
        """
        if not os.path.exists(path) or os.path.isfile(path):
            __logger__.error('Path is invalid')
            sys.exit(1)
        self.print_description(name, path)
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
    def __init__(self, options: dict, name, path):
        """
            : param options : dict
            Oprions, selected by a user
        """
        self.selected_options = options
        self.name = name
        self.path = path

    def build_ledger(self):
        """
        Alpha version, mathces links
        """
        if not os.path.exists(self.path):
            os.mkdir(os.path.join(self.path, self.name))
        # Write code of ledger to path
        self.pw = ProlificWriter(os.path.join(self.path, self.name),
                                 self.selected_options)
        self.pw.write()
        return self.match_links()

    def match_links(self):
        """
        Alpha version, mathces links
        Prints links mathced by user's choose
        """
        res = {}
        for k, v in self.selected_options.items():
            res[v] = LINKS[v]
        print_nested(res, 1)


def arg_parser() -> object:
    """
        Argument parser
    :return: object
        argparse namespace object
    """
    parser = argparse.ArgumentParser(description='GSL execution script')
    parser.add_argument('--init', action='store_true')
    parser.add_argument('--name', action='store', dest='NAME', required=False)
    parser.add_argument('--path', action='store', dest='PATH', required=False)

    return parser.parse_args()


def main() -> None:
    """
    Main entry for program
    """
    args = arg_parser()
    if not args.init:
        __logger__.error('NOT initializing a ledger since `--init` argument was not provided.')
        sys.exit(1)
    __logger__.info('Start Goodsteel Ledger: a program for generating distributed ledgers')
    config_path = DEFAULT_CONFIG_PATH
    kr = Krinkle(config_path)
    options = kr.prompt(name=args.NAME, path=args.PATH)
    __logger__.info('Start getting your ledger\'s algorithms')
    time.sleep(0.5)
    jq = Jarquai(options, args.NAME, args.PATH)
    jq.build_ledger()


if __name__ == '__main__':
    main()

