# AutoZoom
Automatically connect to Zoom meetings through a script.
Inspired by [this](https://github.com/BigchillRK/Zoom-Meeting-and-Recording). If you have any problems or feature suggestions, please submit an issue.
## Overview
Use this to automatically connect to Zoom meetings from the command line. Note, this only works on Linux at the moment.

## Installation
Make sure you have Python3. Also, you'll need the following packages:
* pyautogui
* opencv
* python-crontab (Linux only)
* cron_descriptor (Linux only)

You can install this with the following commands):
### Linux
```
pip3 install pyautogui opencv-python python-crontab cron_descriptor
```

### Windows
```
pip3 install pyautogui opencv-python
```

## Usage
```
usage: autozoom.py [-h] {join,schedule,unschedule,list} ...
```
You can use AutoZoom to join, list, and schedule meetings from the command line.
### Joining
You can use AutoZoom to join to a meeting
```
usage: autozoom.py join [-h] [-f FIX_DROP_DOWN] [-a] [-V] [-v] [-n NAME]
                        [-p PASSWORD] [-r]
                        id

positional arguments:
  id                    The id of the meeting to join

optional arguments:
  -h, --help            show this help message and exit
  -f FIX_DROP_DOWN, --fix-drop-down FIX_DROP_DOWN
                        Use one less tab when joining. See Meeting ID Dropdown
                        for more info
  -a, --audio           Whether or not to turn on your audio input. Default is
                        false.
  -V, --video           Whether or not to turn on your video input. Default is
                        false.
  -v, --verbose         Enable verbose logging. WIP
  -n NAME, --name NAME  The name to display to others.
  -p PASSWORD, --password PASSWORD
                        The password of the meeting to join
  -r, --record          Whether or not to record the call. Default is false.
                        WIP
```
##### Examples
Join meeting with id '1234567890', password 'abcde6' and the name 'John Smith':
```
python3 autozoom.py join 1234567890 -p abcde6 -n 'John Smith'
```
Join meeting with id '421234569' with audio, video, and record:
```
python3 autozoom.py join 421234569 -a -V -r
```

### Schedules (Linux only, Windows coming soon)
#### Basic Scheduling
You can use AutoZoom to schedule meetings following your own CRON schedule (Linux only) or based on days of the week and times.
```
usage: autozoom.py schedule [-h] [-f FIX_DROP_DOWN] [-a] [-V] [-v] [-n NAME]
                            [-p PASSWORD] [-r] (-c CRON | -dt DATETIME)
                            schedulename id

positional arguments:
  schedulename          The name of the schedule to add, i.e. HIS101
  id                    The id of the meeting to join

optional arguments:
  -h, --help            show this help message and exit
  -f FIX_DROP_DOWN, --fix-drop-down FIX_DROP_DOWN
                        Use one less tab when joining. See Meeting ID Dropdown
                        for more info
  -a, --audio           Whether or not to turn on your audio input. Default is
                        false.
  -V, --video           Whether or not to turn on your video input. Default is
                        false.
  -v, --verbose         Enable verbose logging. WIP
  -n NAME, --name NAME  The name to display to others.
  -p PASSWORD, --password PASSWORD
                        The password of the meeting to join
  -r, --record          Whether or not to record the call. Default is false.
                        WIP
  -c CRON, --cron CRON  Custom CRON schedule. (* * * * *). Only use if you
                        know what you're doing. Linux only
  -dt DATETIME, --datetime DATETIME
                        Days of the week (umtwrfs) and the time (24 hour or
                        am/pm). ex. Class at 10:45am on Monday, Wednesday, and
                        Friday (-dt 'mwf 10:45am')
```
##### Examples
Schedule meeting named 'Intro to Databases' on Monday, Tuesday, Thursday, Sunday at 3:30 pm with id 123456789, password abcde6 and record:
```
python3 autozoom.py schedule 'Intro to Databases' 123456789 -p abcde6 -dt "mtru 3:30pm" -r
```

#### Unscheduling (WIP)
You can unschedule individual meetings or all meetings.
```
usage: autozoom.py unschedule [-h] schedulename

positional arguments:
  schedulename  The name of the schedule to remove. Use 'all' to remove all
                schedules., i.e. HIS101
```
##### Examples
Unschedule all meetings
```
python3 autozoom.py unschedule all
```
Unschedule a meeting named 'Introduction to Programming'
```
python3 autozoom.py unschedule 'Introduction to Programming'
```

#### Listing (WIP)
You can list all scheduled meetings.
```
usage: autozoom.py unschedule [-h] schedulename

positional arguments:
  schedulename  The name of the schedule to remove. Use 'all' to remove all
                schedules., i.e. HIS101
```
To list all scheduled meetings, run:
```
python3 autozoom.py list dummyid
```

## Considerations
Due to this tool pressing buttons and looking from them on the computer screen, your system must be logged in and on.

## Small Workarounds
### Unsupported resolutions
If your resolution is not supported, you can go through and manually screenshot the Zoom components yourself:
1. Create a folder named YOURWIDTHxYOURHEIGHT on Linux, YOURWIDTHxYOURHEIGHTwindows on Windows
2. Look at the other folders pictures and capture the same components using a screen capture tool. (Windows+Shift+S works well for Windows)
3. Name accordingly and place them in your folder from step 1.
**Note that btnLeave.png is the blue button on the 'Invalid meeting id window'
  
### Meeting ID Dropdown
Sometimes, if you use Zoom a lot, it will add a little 'V' to the meeting ID field. autozoom.py defaults to working with this. If you don't have it, you can join a bunch of meetings to get it.

### Dual Monitors on Windows
Currently, dual monitor support for Windows does not work well. If you have 2 monitors, make sure Zoom starts on your primary one. Otherwise, Pyautogui is not able to locate the buttons

## Upcoming Features
* Autoscheduling meetings
* Recording (quietly)
* Better Resolution independence (Currently support 1920x1080, 1440x2560, 3840x2160)
