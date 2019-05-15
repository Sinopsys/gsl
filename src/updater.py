#!/usr/bin/env python3.6

import subprocess
from technologies import TOINSTALL, UPDATE_LINKS


for alg, src in UPDATE_LINKS.items():
    p = subprocess.Popen(['bash', 'pull_single.sh', f'{TOINSTALL[alg]}', f'{src}'], stdout=subprocess.PIPE)
    (result, error) = p.communicate()
    print(result.decode())
