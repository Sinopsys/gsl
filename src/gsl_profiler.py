import os
import sys
import subprocess
from technologies import TOINSTALL, INTERFACES, OPTIONS
from goodsteel_ledger import Jarquai


class Profiler(object):
    def __init__(self):
        self.starting_port = 4999

    def get_all_algs(self, alg):
        res = []
        for item in OPTIONS[alg]:
            if item in TOINSTALL.keys():
                res.append(item)
        return res

    def create_ledger(self, options, name, path, t):
        jq = Jarquai(options, name, path, t, True)
        jq.build_ledger()

    def measure_all(self):
        port = self.starting_port + 1
        import_path = os.path.join(self.path, self.name)
        os.system('sed -ir "0,/def _portd/{s/_portd = .*/_portd = ' + str(port) + '/}" ' + os.path.join(import_path, 'miner.py'))
        os.system('sed -ir "0,/def _portd/{s/_portd = .*/_portd = ' + str(port) + '/}" ' + os.path.join(import_path, 'wallet.py'))
        if import_path not in sys.path:
            sys.path.append(import_path)
        import miner
        import wallet
        miner.run()
        wallet._profile_timings()
        pass

    def measure_all_times(self, path):
        self.path = path
        self.name = 'gsl_profiling'
        hashes = self.get_all_algs('hashing')
        dss = self.get_all_algs('digital signature')
        for hash_ in hashes:
            for ds_ in dss:
                options = {'hashing': hash_, 'digital signature': ds_}
                self.create_ledger(options, self.name, path, True)
                self.measure_all()
                pass

    def _pip_install_(self, package):
        subprocess.call([sys.executable, '-m', 'pip', 'install', package])

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
        subprocess.call([sys.executable, f'{path}/setup.py', 'install'])

