import pyautogui 
import time
import sys
import os
import argparse
import locate
import platform

PLATFORM = 0
LINUX = 1
WINDOWS = 2

plat = platform.platform().lower()

if 'linux' in plat:
    PLATFORM = LINUX
elif 'windows' in plat:
    PLATFORM = WINDOWS

def restartZoom():
    global PLATFORM
    if PLATFORM == LINUX:
        os.system("ps aux | grep zoom | grep autozoom -v |  awk '{print $2}' | xargs kill")
        time.sleep(1)
        os.system('/usr/bin/zoom &')
    elif PLATFORM == WINDOWS:
        os.system("for /f \"tokens=2\" %A in ('tasklist ^| findstr /i \"Zoom\" 2^>NUL') do taskkill /F /PID %A")
        time.sleep(1)
        os.startfile(os.getenv('APPDATA') + '\\Zoom\\bin\\Zoom.exe')
    else:
        print('Error: Unsupported operating system: {}. Please submit an issue'.format(plat))
        exit(1)
    
parser = argparse.ArgumentParser(description="Automatically connect to a Zoom call")
parser.add_argument("id", help="The id of the meeting to join", type=str)

parser.add_argument("-a", "--audio", help="Enable the audio", action="store_true")
parser.add_argument("-V", "--video", help="Enable video", action="store_true")
parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
parser.add_argument("-n", "--name", help="The name to display", type=str)

parser.add_argument("-p", "--password", help="The password to use", type=str)
parser.add_argument("-r", "--record", help="Enable recording of the call", action="store_true")


args = parser.parse_args()
#Kill Zoom and restart
#We need to inverse it so it doesn't kill the current process
restartZoom()
time.sleep(3)

x,y = locate.locate('btnJoin')
pyautogui.click(x,y)
time.sleep(3)

#Enter meeting id
x,y = locate.locate('txtId')
pyautogui.click(x,y)
time.sleep(1)
pyautogui.write(args.id)
time.sleep(3)

#GUI varies slightly on Linux systems
#if PLATFORM == LINUX:
pyautogui.press('tab', interval=0.5)
pyautogui.press('tab', interval=0.5)

if args.name:
    pyautogui.press('backspace', 50)
    pyautogui.write(args.name)

pyautogui.press('tab', interval=0.5)

#Set audio enable
if not args.audio:
    pyautogui.press('enter', interval=0.5)

pyautogui.press('tab', interval=0.5)

#Set video enable
if not args.video:
    pyautogui.press('enter', interval=0.5)

#Navigate to the next screen
pyautogui.press('tab', interval=0.5)
pyautogui.press('enter',interval=1)

#Password
if args.password:
    time.sleep(3)

    #Check for error message
    result = locate.locate('errorid')

    #If there is an error message, remove it
    if result:
        x, y = locate.locate('btnLeave')
        pyautogui.click(x,y)
        time.sleep(3)

    result = locate.locate('txtPass')

    #If the error was actuall fake, and password thing is there, enter the password
    if result:
        x, y = result
        pyautogui.click(x,y)
        time.sleep(2)
        pyautogui.write(args.password)
        time.sleep(2)

        pyautogui.press('tab', interval=0.5)
        pyautogui.press('enter',interval=1)
    else:
        print('Fatal error occured. Invalid meeting id.')
