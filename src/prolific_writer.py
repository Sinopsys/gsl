"""
Prolific Writer
"""

import os
import sys
import subprocess
from inspect import getsource
from shutil import copyfile
from technologies import _kv_, get
from target_dummy import wallet
from target_dummy import miner
TOINSTALL = _kv_.TOINSTALL
INTERFACES = _kv_.INTERFACES


class ProlificWriter(object):
    def __init__(self, full_path, opts, timed, profd=False):
        self.path = full_path
        self.opts = opts
        self.timed = timed
        self.profd = profd

    def write(self):
        # WRITE ALGORITHMS ITSELF
        #
        self._write_hashing_()
        self._write_digital_signature_()

        self._write_(wallet)
        self._write_(miner)

    def _write_(self, script_to_write):
        name = f'{script_to_write.__name__.split(".")[-1]}.py'
        src_code = getsource(script_to_write)
        with open(os.path.join(self.path, name), 'w') as __fd__:
            __fd__.write(src_code)
        if self.timed:
            os.system('sed -ir "0,/def _timed/{s/_timed = .*/_timed = True/}" ' + os.path.join(self.path, name))
        if self.profd:
            os.system('sed -ir "0,/def _profd/{s/_profd = .*/_profd = True/}" ' + os.path.join(self.path, name))

    def _get_src_path_(self):
        path = sys.path
        for p in path:
            if 'gsl/src' in p:
                return p

    def _pip_install_(self, package):
        subprocess.call([sys.executable, '-m', 'pip', 'install', package, '--user'])

    def _install_(self, path):
        """
        Installs with `python setup.py install`
        """
        if 'ecdsa' in path.lower():
            self._pip_install_('ecdsa')
            return
        elif 'x11' in path.lower():
            self._pip_install_('x11_hash')
            return
        elif 'x17' in path.lower():
            self._pip_install_('x17_hash')
            return
        os.chdir(path)
        subprocess.call([sys.executable, f'{path}/setup.py', 'install', '--user'])

    def _write_hashing_(self):
        # INSTALLING PROCEDURE
        src_path = self._get_src_path_()
        path = os.path.join(src_path, get('TOINSTALL', self.opts['hashing']))
        self._install_(path)

        # WRITING PROCEDURE
        name = 'myhashing.py'
        type_ = self.opts['hashing']
        path = os.path.join(src_path, get('INTERFACES', type_), name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        copyfile(path, os.path.join(self.path, name))

    def _write_digital_signature_(self):
        # INSTALLING PROCEDURE
        src_path = self._get_src_path_()
        path = os.path.join(src_path, get('TOINSTALL', self.opts['digital signature']))
        self._install_(path)

        # WRITING PROCEDURE
        name = 'mydss.py'
        type_ = self.opts['digital signature']
        path = os.path.join(src_path, get('INTERFACES', type_), name)
        copyfile(path, os.path.join(self.path, name))


# EOF
