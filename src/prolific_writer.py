"""
Prolific Writer
"""

import os
import sys
import subprocess
from inspect import getsource
from technologies import TOINSTALL
import example_chain
from target_dummy import wallet
from target_dummy import miner


class ProlificWriter(object):
    def __init__(self, full_path, opts):
        self.path = full_path
        self.opts = opts

    def write(self):
        # WRITE ALGORITHMS ITSELF
        #
        self._write_hashing_()
        self._write_digital_signature_()

        with open(os.path.join(self.path, 'myhashing.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['hashing']))

        with open(os.path.join(self.path, 'mydigital_signature.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['digital signature']))

        with open(os.path.join(self.path, 'myconsensus.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['consensus']))

        self._write_(wallet)
        self._write_(miner)

    def _write_(self, script_to_write):
        name = f'{script_to_write.__name__.split(".")[-1]}.py'
        src_code = getsource(script_to_write)
        with open(os.path.join(self.path, name), 'w') as __fd__:
            __fd__.write(src_code)

    def _get_src_path_(self):
        path = sys.path
        for p in path:
            if 'gsl/src' in p:
                return p

    def _install_(self, path):
        """
        Installs with `python setup.py install`
        """
        if 'ecdsa' in path.lower():
            subprocess.call([sys.executable, '-m', 'pip', 'install', 'ecdsa'])
            return
        os.chdir(path)
        subprocess.call([sys.executable, f'{path}/setup.py', 'install'])

    def _write_hashing_(self):
        src_path = self._get_src_path_()
        path = os.path.join(src_path, TOINSTALL[self.opts['hashing']])
        print(path)
        self._install_(path)

    def _write_consensus_(self):
        pass

    def _write_digital_signature_(self):
        src_path = self._get_src_path_()
        path = os.path.join(src_path, TOINSTALL[self.opts['digital signature']])
        print(path)
        self._install_(path)


# EOF
