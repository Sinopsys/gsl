#!/usr/bin/env python3.6

import subprocess
from technologies import _kv_, get
TOINSTALL = _kv_.TOINSTALL
UPDATE_LINKS = _kv_.UPDATE_LINKS

for alg, src in UPDATE_LINKS.items():
    p = subprocess.Popen(['bash', 'pull_single.sh', f'{get("TOINSTALL", alg)}', f'{src}'], stdout=subprocess.PIPE)
    (result, error) = p.communicate()
    print(result.decode())
