# AutoZoom
Automatically connect to Zoom meetings through a script
## Overview
Use this to automatically connect to Zoom meetings from the command line. Note, this only works on Linux at the moment.

## Installation
Make sure you have Python3. Also, you'll need the following packages:
* pyautogui
You can install this with the following command:
`pip3 install pyautogui`

## Usage
```
usage: autozoom.py [-h] [-a AUDIO] [-V VIDEO] [-v VERBOSE] [-n NAME]
                   [-p PASSWORD] [-r RECORD]
                   id
```
Ex. To connect to a meeting with id 1234567890, password abcde6 and the name John Smith:
```
python3 autozoom.py 1234567890 -p abcde6 -n "John Smith"
```

## Upcoming
* Windows support
* Autoscheduling meetings
* Recording (quietly)
