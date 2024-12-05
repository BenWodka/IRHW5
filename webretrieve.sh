#!/bin/bash

command="$1"
shift

lineCountDict=$(wc -l < outfiles/dict.txt)

python3 webretrieve.py "$command" "$@" "$lineCountDict"
