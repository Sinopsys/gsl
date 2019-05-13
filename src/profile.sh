#!/usr/bin/env bash

for i in {1..24}
do
    export num=$i
    python goodsteel_ledger.py --profile-all True --name myledger --path ~/tmp/gsl
done

# EOF
