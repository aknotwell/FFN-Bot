#!/bin/sh
# Wrapper around main python program to prevent credential leak to github. 
# $1 is the path to the venv -- defaults to myvenv

if [ $# -eq 0 ]
then
   VENV=myvenv
else
   VENV="$1"
fi

source startup.env
source $VENV/bin/activate
python3 main.py
