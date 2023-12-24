#!/bin/bash
PID=`ps -ef | grep "/bin/bash /home/pi/misc/server-start-terraria.sh" | grep -v grep | awk '{print $2}'`
kill -2 -$PID
