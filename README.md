# gsl

[![Run Status](https://api.shippable.com/projects/5cbc3edfdaf54c0007d7bbd1/badge?branch=master)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


gsl -- Goodsteel ledger. Krinkle Goodsteel will help you to build your own distributed ledger.

## Installation
Execute following commands linebyline
```bash
git clone https://github.com/Sinopsys/gsl.git
cd gsl
export PYTHONPATH=$PYTHONPATH"$(pwd)/src"
[[ $PATH != *".local/bin"* ]] && export PATH=$PATH":/home/$USER/.local/bin"
echo "mkdir /tmp/gsl" && mkdir /tmp/gsl
echo "sudo mkdir /etc/gsl" && sudo mkdir /etc/gsl
echo "sudo cp ./example_config.yaml /etc/gsl/config.yaml" && sudo cp ./example_config.yaml /etc/gsl/config.yaml

python3.6 -m pip install . --user

## OPTIONAL, if you do not want to set it manually every time
## Just echoes above exports to your $SHELLrc file
rc_file="/home/$USER/.$(echo $SHELL | rev | cut -d / -f 1 | rev)rc"
echo "export PATH=\$PATH\":/home/$USER/.local/bin\"" >> $rc_file
echo "export PYTHONPATH=\$PYTHONPATH\":$(pwd)/src/\"" >> $rc_file
```

Then, to successfully launch app, it is needed to have a config with path
`/etc/gsl/config.yaml`. During installation, an example config has already been
put to that path.

Example `config.yaml`:
```
# Key init_dir is path where your blockchain will be stored.
#
init_dir: /tmp/gsl
```

## Usage

```
$    gsl --init --name NAME [--path PATH] # path can also be taken from config.
```

## Questions
Write kupriyanovkirill@gmail.com, mephisto@openmail.cc, https://t.me/SsinopsysS, or create an issue


