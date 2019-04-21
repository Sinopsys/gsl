"""
    Init script for creating ledger.
"""
import sys
import os
import yaml
import logging.config

from utils.log import LOG_CONFIG
from utils.output import print_nested

LOGGING = logging.config.dictConfig(LOG_CONFIG)
__logger__ = logging.getLogger('stdout')


class Jarquai(object):
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        return config.load(self.config_path)

    def prompt():
        print('')


def main() -> None:
    __logger__.info('Start Goodsteel Ledger: a program for generating distributed ledgers')
    config_path = '.'
    jq = Jarquai(config_path)


if __name__ == '__main__':
    main()

