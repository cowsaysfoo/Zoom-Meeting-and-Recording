# AutoZoom
Automatically connect to Zoom meetings through a script.
Inspired by [this](https://github.com/BigchillRK/Zoom-Meeting-and-Recording).
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
usage: autozoom.py [-h] [-f FIX_DROP_DOWN] [-a] [-V] [-v] [-n NAME]
                   [-p PASSWORD] [-r] [-s SCHEDULENAME] [-c CRON] [-d DAYS]
                   [-t TIME]
                   {join,schedule,unschedule} id
```
### Connecting
Ex. To connect to a meeting with id 1234567890, password abcde6 and the name John Smith:
```
python3 autozoom.py join 1234567890 -p abcde6 -n "John Smith"
```

### Schedules (Linux only, Windows coming soon)
#### Basic Scheduling
Ex. To schedule a class on Monday, Wednesday, Friday at 3:30 pm with id 123456789, password abcde6 and name CS216:
```
python3 autozoom.py schedule 123456789 -p abcde6 -d mwf -t "3:30pm" -s CS216
```

#### Unscheduling (WIP)
(Note these need a 'dummy id' for now while the argument system is reworked)
To remove, simply run:
```
python3 autozoom.py unschedule dummyid -s CS216
```

#### Listing (WIP)
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
