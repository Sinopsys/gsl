"""
Prolific Writer
"""

import os
from inspect import getsource
import example_chain
from target_dummy import wallet
from target_dummy import miner


class ProlificWriter(object):
    def __init__(self, full_path, opts):
        self.path = full_path
        self.opts = opts

    def write(self):
        self._write_(wallet)
        self._write_(miner)

    def _write_(self, script_to_write):
        name = f'{script_to_write.__name__.split(".")[-1]}.py'
        src_code = getsource(script_to_write)
        with open(os.path.join(self.path, name), 'w') as __fd__:
            __fd__.write(src_code)

        # WRITE ALGORITHMS ITSELF
        #
        with open(os.path.join(self.path, 'my_hashing.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['hashing']))

        with open(os.path.join(self.path, 'my_digital_signature.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['digital signature']))

        with open(os.path.join(self.path, 'my_consensus.py'), 'w') as __fd__:
            __fd__.write(str(self.opts['consensus']))


# EOF
