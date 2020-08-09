#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $DIR

echo "Killing zoom"
ps aux | grep zoom | grep -v autozoom | awk '{print $2}' | xargs kill
echo "Starting zoom"
DISPLAY=:0 /usr/bin/zoom &

DISPLAY=:0 konsole --workdir "$DIR" -e bash -c "$@"
