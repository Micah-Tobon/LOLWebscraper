#!/usr/bin/env bash
DIR="$( cd "$( dirname "$0" )" && pwd )"

cd "${DIR%}"
pwd

python3 -m venv macenv
source macenv/bin/activate
pip install -r macrequirements.txt 
python3 webscraper.py
