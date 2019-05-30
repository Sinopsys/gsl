#!/usr/bin/env bash
echo "Actions will be echoed before executing"
if [[ $PATH != *".local/bin"* ]]; then
    echo ""
    echo "Setting PATH variable securely"
    echo 'export PATH=\$PATH":/home/$USER/.local/bin"' >> /home/$USER/.zshrc
    export PATH=$PATH":/home/$USER/.local/bin"
    echo ""
fi
if [[ $PYTHONPATH != *"gsl"* ]]; then
    echo "Setting PYTHONPATH variable securely"
    echo 'export PYTHONPATH=\$PYTHONPATH":$(pwd)/src/"' >> /home/$USER/.zshrc
    export PYTHONPATH=$PYTHONPATH":$(pwd)/src/"
fi
echo "mkdir /tmp/gsl"
mkdir /tmp/gsl
echo "sudo mkdir /etc/gsl"
sudo mkdir /etc/gsl
echo "sudo cp ./example_config.yaml /etc/gsl/config.yaml"
sudo cp ./example_config.yaml /etc/gsl/config.yaml


# EOF

