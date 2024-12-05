#!/bin/bash

command="$1"
shift

lineCountDict=$(wc -l < outfiles/dict.txt)

python3 retrieve.py "$command" "$@" "$lineCountDict"
