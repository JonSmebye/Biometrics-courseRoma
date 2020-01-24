#!/bin/bash

while true; do
	if [ $(ps -efa | grep -v grep | grep firefox -c) -gt 0 ]; then
		python3 /Users/jonsmebye/Documents/skole/biometric/faceDetection.py
		printf "firefox running\n"
	else
		printf "firefox not running\n"
	fi
	sleep 5
done