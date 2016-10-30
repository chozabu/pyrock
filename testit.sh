#!/usr/bin/env bash
source env/bin/activate
python main.py &
python main.py --settingsfile settingsalt.json

kill $!