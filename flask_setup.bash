#!/bin/bash

# usage: ./flask_setup.bash VIRTUAL_ENV_ACTIVATE_SCRIPT

source $1
pip install --upgrade pip
pip install flask
deactivate

