#!/usr/bin/env bash
source env/bin/activate
python main.py --test-mode --no-auto &
python main.py --settingsfile settingsalt.json --test-mode

kill $!
