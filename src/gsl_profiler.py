import os
import sys
import requests
import itertools
import json
import subprocess
from technologies import _kv_, get
from goodsteel_ledger import Jarquai

TOINSTALL = _kv_.TOINSTALL
OPTIONS = _kv_.OPTIONS


class Profiler(object):
    def __init__(self):
        pass

    def get_all_algs(self, alg):
        res = []
        for item in get('OPTIONS', alg):
            if item in TOINSTALL.keys():
                res.append(item)
        return res

    def create_ledger(self, options, name, path, t):
        jq = Jarquai(options, name, path, t, True)
        jq.build_ledger()

    def measure_all(self):
        port = 5000
        import_path = os.path.join(self.path, self.name)
        os.system('sed -ir "0,/def _portd/{s/_portd = .*/_portd = ' + str(port) + '/}" ' + os.path.join(import_path, 'miner.py'))
        os.system('sed -ir "0,/def _portd/{s/_portd = .*/_portd = ' + str(port) + '/}" ' + os.path.join(import_path, 'wallet.py'))
        # if import_path not in sys.path:
        #     sys.path.append(import_path)
        # import miner
        # import wallet
        # miner.full_run()
        # wallet._profile_timings()
        # reloaded = requests.get('http://localhost:' + str(port) + '/reload')
        # print('\n\n\n\n')
        # print(reloaded.content)
        # print('\n\n\n\n')
        # pass

    def measure_all_times(self, path):
        self.path = path
        self.name = 'gsl_profiling'
        hashes = self.get_all_algs('hashing')
        dss = self.get_all_algs('digital signature')
        num = int(os.environ['ALGS_NUM'])
        pairs = list(itertools.product(hashes, dss))[num]
        options = {'hashing': pairs[0], 'digital signature': pairs[1]}
        self.create_ledger(options, self.name, path, True)
        self.measure_all()
        # for hash_ in hashes:
        #     for ds_ in dss:
        #         options = {'hashing': hash_, 'digital signature': ds_}
        #         self.create_ledger(options, self.name, path, True)
        #         self.measure_all()
        #         pass

    def _pip_install_(self, package):
        subprocess.call([sys.executable, '-m', 'pip', 'install', package])

    def _install_(self, path):
        """
        Installs with `python setup.py install`
        """
        # CRY HAVOC
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

