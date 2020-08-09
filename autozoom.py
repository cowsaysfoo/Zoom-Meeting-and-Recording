import pyautogui 
import time
import sys
import os
import argparse
import locate
from platforms import getPlatform, LINUX, WINDOWS
import connecting
import scheduling

def join(args):
    connecting.connect(args.id, args.password, args.audio, args.video, args.name)

def schedule(args):
    if args.cron:
        scheduling.cronSchedule(args.schedulename, args.cron, args.id, args.password, args.audio, args.video, args.record, args.name)
    else:
        split = args.datetime.split(' ')
        days = split[0]
        time = ' '.join(split[1:])

        scheduling.dayTimeSchedule(args.schedulename, days, time, args.id, args.password, args.audio, args.video, args.record, args.name)

def unschedule(args):
    scheduling.cronUnschedule(args.schedulename)

def listschedule(args):
    scheduling.listSchedule()
    
parser = argparse.ArgumentParser(description='Join or schedule Zoom calls from the command line')
commandparsers = parser.add_subparsers(title='Commands', description='Subcommands', help='Either join, schedule, list, or unschedule')

joinparser = commandparsers.add_parser('join', help='Join a Zoom meeting')
joinparser.add_argument("id", help="The id of the meeting to join", type=str)
joinparser.add_argument("-f", "--fix-drop-down", help="Use one less tab when joining. See Meeting ID Dropdown for more info", default=False)
joinparser.add_argument("-a", "--audio", help="Enable the audio", action="store_true", default=False)
joinparser.add_argument("-V", "--video", help="Enable video", action="store_true", default=False)
joinparser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
joinparser.add_argument("-n", "--name", help="The name to display", type=str, default='')
joinparser.add_argument("-p", "--password", help="The password to use", type=str, default='')
joinparser.add_argument("-r", "--record", help="Enable recording of the call", action="store_true", default=False)
joinparser.set_defaults(func=join)

scheduleparser = commandparsers.add_parser('schedule', help='Schedule Zoom meetings')
scheduleparser.add_argument('schedulename', help='The name of the schedule to add, i.e. HIS101')
scheduleparser.add_argument("id", help="The id of the meeting to join", type=str)
scheduleparser.add_argument("-f", "--fix-drop-down", help="Use one less tab when joining. See Meeting ID Dropdown for more info", default=False)
scheduleparser.add_argument("-a", "--audio", help="Enable the audio", action="store_true", default=False)
scheduleparser.add_argument("-V", "--video", help="Enable video", action="store_true", default=False)
scheduleparser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
scheduleparser.add_argument("-n", "--name", help="The name to display", type=str, default='')
scheduleparser.add_argument("-p", "--password", help="The password to use", type=str, default='')
scheduleparser.add_argument("-r", "--record", help="Enable recording of the call", action="store_true", default=False)

timegroup = scheduleparser.add_mutually_exclusive_group(required=True)
timegroup.add_argument("-c", "--cron", help="Input the CRON schedule manually. Linux only", type=str)
timegroup.add_argument("-dt", "--datetime", help="Days of the week (umtwrfs) and the time (24 hour or am/pm). i.e. 'mwf 10:45am'")

scheduleparser.set_defaults(func=schedule)

unscheduleparser = commandparsers.add_parser('unschedule', help='Unschedule Zoom meetings')
unscheduleparser.add_argument('schedulename', help='The name of the schedule to remove. Use \'all\' to remove all schedules., i.e. HIS101')
unscheduleparser.set_defaults(func=unschedule)


listparser = commandparsers.add_parser('list', help='List all scheduled Zoom meetings')
listparser.set_defaults(func=listschedule)

args = parser.parse_args()
args.func(args)

    #
#action = args.action
#
#if action == 'join':
#    connecting.connect(args.id, args.password, args.audio, args.video, args.name)
#
#elif action == 'schedule':
#    if args.cron:
#        scheduling.cronSchedule(args.schedulename, args.cron, args.id, args.password, args.audio, args.video, args.record, args.name)
#    else:
#       scheduling.dayTimeSchedule(args.schedulename, args.days, args.time, args.id, args.password, args.audio, args.video, args.record, args.name)
#
#elif action == 'list':
#    scheduling.listSchedule()
#
#elif action == 'unschedule':
#   scheduling.cronUnschedule(args.schedulename)
