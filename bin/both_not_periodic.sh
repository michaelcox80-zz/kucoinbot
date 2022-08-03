#!/bin/bash

# source FULL_PATH_TO_VIRTUALENV
# example : 
source /home/pmpls13/python-virtual-environments/kucoin/bin/activate
# Leave line commented if not using virtualenv

python3 ../kucoin/kucoin/runner.py "false" &
python3 ../gateio/gateio/runner.py "false"