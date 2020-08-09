import pyautogui 
import time
import sys
import os
import argparse
import locate
from platforms import getPlatform, LINUX, WINDOWS
import connecting
import scheduling

def restartZoom():
    if getPlatform() == LINUX:
        os.system("ps aux | grep zoom | grep autozoom -v |  awk '{print $2}' | xargs kill")
        time.sleep(1)
        os.system('/usr/bin/zoom &')
    elif getPlatform() == WINDOWS:
        os.system("for /f \"tokens=2\" %A in ('tasklist ^| findstr /i \"Zoom\" 2^>NUL') do taskkill /F /PID %A")
        time.sleep(1)
        os.startfile(os.getenv('APPDATA') + '\\Zoom\\bin\\Zoom.exe')
    else:
        print('Error: Unsupported operating system: {}. Please submit an issue'.format(plat))
        exit(1)
    
parser = argparse.ArgumentParser(description="Automatically connect to a Zoom call")
parser.add_argument("action", choices=['join', 'schedule', 'unschedule'], help="Action to perform")
parser.add_argument("id", help="The id of the meeting to join", type=str)

parser.add_argument("-f", "--fix-drop-down", help="Use one less tab when joining. See Meeting ID Dropdown for more info", default=False)
parser.add_argument("-a", "--audio", help="Enable the audio", action="store_true", default=False)
parser.add_argument("-V", "--video", help="Enable video", action="store_true", default=False)
parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
parser.add_argument("-n", "--name", help="The name to display", type=str, default='')

parser.add_argument("-p", "--password", help="The password to use", type=str, default='')
parser.add_argument("-r", "--record", help="Enable recording of the call", action="store_true", default=False)

parser.add_argument("-s", "--schedulename", help="The name for this schedule", type=str)
parser.add_argument("-c", "--cron", help="Input the CRON schedule manually. Only on Linux.", type=str)
parser.add_argument("-d", "--days", help="Days to do the call", type=str)
parser.add_argument("-t", "--time", help="Time to do the call", type=str)


args = parser.parse_args()

action = args.action

if action == 'join':
    connecting.connect(args.id, args.password, args.audio, args.video, args.name)
    
elif action == 'schedule':
    if args.cron:
        scheduling.cronSchedule(args.schedulename, args.cron, args.id, args.password, args.audio, args.video, args.record, args.name)
    else:
       scheduling.dayTimeSchedule(args.schedulename, args.days, args.time, args.id, args.password, args.audio, args.video, args.record, args.name)

elif action == 'unschedule':
   scheduling.cronUnschedule(args.schedulename)
