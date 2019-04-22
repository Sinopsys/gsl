# gsl

[![Run Status](https://api.shippable.com/projects/5cbc3edfdaf54c0007d7bbd1/badge?branch=master)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


gsl -- Goodsteel ledger. Krinkle Goodsteel will help you to build your own distributed ledger.

## Installation
```
$    cd gsl
$    export PYTHONPATH=$PYTHONPATH"$(pwd)/src"
$    pip3 install . --user
```

Then, to successfully launch app, it is needed to have a config with path
`/home/$USER/.gsl/config.yaml`

Example `config.yaml`:
```
# Example and debug configuration
#
init_dir: /home/coldmind/Projects/gsl/result # At the moment, ANY directory will be OK
```

## Usage

```
$    gsl
```

## Questions
Write kupriyanovkirill@gmail.com, mephisto@openmail.cc, https://t.me/SsinopsysS, or create an issue


### TODO
* Add implementations of all algorithms
* Find out about code licenses for algorithms to use
* `argparse`
* Arguments. init (initialize ledger in current dir), name (of the ledger), config (path to gsl's config),
* Documentation, usage in README

