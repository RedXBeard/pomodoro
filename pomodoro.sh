#!/bin/bash -

kivy=$(pip freeze | grep Kivy)
cython=$(pip freeze | grep Cython)

if [ "$kivy" = "" ]; then
	echo "please type; 'pip install git+https://github.com/RedXBeard/kivy.git@red'"
	exit
fi
if [ "$cython" = "" ]; then
	echo "please type; 'pip install Cython'"
	exit
fi

python $(pwd)/pomodoro.py