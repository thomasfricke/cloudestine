#!/bin/bash

set -e

[ -x /usr/bin/virtualenv ] || ( echo "please install virtualenv" && exit 1)

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
