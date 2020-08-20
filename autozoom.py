"""The entry point for autozoom.py, handles argument parsing"""
import argparse
import connecting
import scheduling

def join(args):
    """Runs the 'join' command given args"""
    connecting.connect(args.id, args.password, args.audio, args.video, args.name, args.fixdropdown, args.keytimeout, args.startimeout, args.jointimeout, args.passtimeout)
    print('Exiting')

def schedule(args):
    """Runs the 'schedule' command given args"""
    if args.cron:
        scheduling.cronSchedule(args.schedulename, args.cron, args.id, args.password, args.audio, args.video, args.record, args.name, args.keytimeout, args.starttimeout, args.jointimeout, args.passtimeout)
    else:
        split = args.datetime.split(' ')
        days = split[0]
        time = ' '.join(split[1:])

        scheduling.dayTimeSchedule(args.schedulename, days, time, args.id, args.password, args.audio, args.video, args.record, args.name, args.keytimeout, args.starttimeout, args.jointimeout, args.passtimeout)

def unschedule(args):
    """Runs the 'unschedule' command given args"""
    scheduling.cronUnschedule(args.schedulename)

def listschedule(args):
    """Runs the 'list' command given args"""
    scheduling.listSchedule()
    
PARSER = argparse.ArgumentParser(description='Join or schedule Zoom calls from the command line')
COMMAND_PARSERS = PARSER.add_subparsers(title='Commands', description='Subcommands', help='Either join, schedule, list, or unschedule')

JOIN_PARSER = COMMAND_PARSERS.add_parser('join', help='Join a Zoom meeting')
JOIN_PARSER.add_argument("id",                           help="The id of the meeting to join", type=str)
JOIN_PARSER.add_argument("-f", "--fixdropdown",        help="Use one less tab when joining. See Meeting ID Dropdown for more info", default=False)
JOIN_PARSER.add_argument("-a", "--audio",                help="Whether or not to turn on your audio input. Default is false.", action="store_true", default=False)
JOIN_PARSER.add_argument("-V", "--video",                help="Whether or not to turn on your video input. Default is false.", action="store_true", default=False)
JOIN_PARSER.add_argument("-v", "--verbose",              help="Enable verbose logging. WIP", action="store_true")
JOIN_PARSER.add_argument("-n", "--name",                 help="The name to display to others.", type=str, default='')
JOIN_PARSER.add_argument("-p", "--password",             help="The password of the meeting to join", type=str, default='')
JOIN_PARSER.add_argument("-r", "--record",               help="Whether or not to record the call. Default is false. WIP", action="store_true", default=False)
JOIN_PARSER.add_argument("-kto", "--keytimeout",         help="Amount of time to wait between pressing button/keys.", default=2)
JOIN_PARSER.add_argument("-sto", "--starttimeout",       help="Amount of time to wait for Zoom to start. Increase if running on a slow PC.", default=20)
JOIN_PARSER.add_argument("-jto", "--jointimeout",        help="Amount of time to wait after pressing 'Join' button. Increase if slow internet connection.", default=20)
JOIN_PARSER.add_argument("-pto", "--passtimeout",        help="Amount of time to wait after connection to enter password. Increase if slow internet connection.", default=20)

JOIN_PARSER.set_defaults(func=join)

SCHEDULE_PARSER = COMMAND_PARSERS.add_parser('schedule',  help='Schedule Zoom meetings')
SCHEDULE_PARSER.add_argument('schedulename',             help='The name of the schedule to add, i.e. HIS101')
SCHEDULE_PARSER.add_argument("id",                       help="The id of the meeting to join", type=str)
SCHEDULE_PARSER.add_argument("-f", "--fixdropdown",      help="Use one less tab when joining. See Meeting ID Dropdown for more info", default=False)
SCHEDULE_PARSER.add_argument("-a", "--audio",            help="Whether or not to turn on your audio input. Default is false.", action="store_true", default=False)
SCHEDULE_PARSER.add_argument("-V", "--video",            help="Whether or not to turn on your video input. Default is false.", action="store_true", default=False)
SCHEDULE_PARSER.add_argument("-v", "--verbose",          help="Enable verbose logging. WIP", action="store_true")
SCHEDULE_PARSER.add_argument("-n", "--name",             help="The name to display to others.", type=str, default='')
SCHEDULE_PARSER.add_argument("-p", "--password",         help="The password of the meeting to join", type=str, default='')
SCHEDULE_PARSER.add_argument("-r", "--record",           help="Whether or not to record the call. Default is false. WIP", action="store_true", default=False)
JOIN_PARSER.add_argument("-kto", "--keytimeout",         help="Amount of time to wait between pressing button/keys.", default=2)
SCHEDULE_PARSER.add_argument("-sto", "--starttimeout",   help="Amount of time to wait for Zoom to start. Increase if running on a slow PC.", default=20)
SCHEDULE_PARSER.add_argument("-jto", "--jointimeout",    help="Amount of time to wait after pressing 'Join' button. Increase if slow internet connection.", default=20)
SCHEDULE_PARSER.add_argument("-pto", "--passtimeout",    help="Amount of time to wait after connection to enter password. Increase if slow internet connection.", default=20)

TIME_GROUP = SCHEDULE_PARSER.add_mutually_exclusive_group(required=True)
TIME_GROUP.add_argument("-c", "--cron",          help="Custom CRON schedule. (* * * * *). Only use if you know what you're doing. Linux only", type=str)
TIME_GROUP.add_argument("-dt", "--datetime",     help="Days of the week (umtwrfs) and the time (24 hour or am/pm). ex. Class at 10:45am on Monday, Wednesday, and Friday (-dt 'mwf 10:45am')")

SCHEDULE_PARSER.set_defaults(func=schedule)

UNSCHEDULE_PARSER = COMMAND_PARSERS.add_parser('unschedule', help='Unschedule Zoom meetings based on the schedulename')
UNSCHEDULE_PARSER.add_argument('schedulename', help='The name of the schedule to remove. Use \'all\' to remove all schedules., i.e. HIS101')
UNSCHEDULE_PARSER.set_defaults(func=unschedule)


LIST_PARSER = COMMAND_PARSERS.add_parser('list', help='List all scheduled Zoom meetings')
LIST_PARSER.set_defaults(func=listschedule)

ROOT_ARGS = PARSER.parse_args()

try:
    ROOT_ARGS.func(ROOT_ARGS)
except Exception as e:
    print(e)
    print('Please provide a command {join, schedule, unschedule, list}')
    exit(1)
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
