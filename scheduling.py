"""Used to automatically schedule meetings through CRON or Windows equivalent"""
import getpass
from dateutil import parser
from crontab import CronTab

PREFIX = 'AUTOZOOM'

def get_full_path():
    """Gets the full path of the executed file"""
    return __file__.replace('scheduling', 'autozoom')

def day_time_to_cron(days, time):
    """Converts time to cron, i.e. "mwf 10:00pm" to cron equivalent"""
    days = days.lower()
    for c in days:
        if not c in 'umtwrfs':
            raise Exception('Invalid date string. Must only contain umtwrfs.')

    day_key = list('umtwrfs')
    date = parser.parse(time)
    cron_days = ','.join([str(day_key.index(d)) for d in days])
    minute = date.minute
    hour = date.hour

    return '{} {} * * {}'.format(minute, hour, cron_days)

def args_to_cmd(path, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    """Creates a command given the arguments"""
    return '{} "python3 {} join {}"'.format(path.replace('autozoom.py', 'cronLauncher.sh'), path, id) + ' ' + ' '.join([('--name '.format(name) if name else ''), ('--password {}'.format(password) if password else ''), ('--audio' if audio else ''), ('--Video' if video else ''), ('--record' if record else ''), ('--keytimeout {}'.format(keytimeout) if keytimeout else ''), ('--starttimeout {}'.format(starttimeout) if starttimeout else ''), ('--jointimeout {}'.format(jointimeout) if jointimeout else ''), ('--passtimeout {}'.format(passtimeout) if passtimeout else '')])

def create_cron_line(name, cron, cmd):
    """Create the raw cron lines for the crontab file"""
    global PREFIX
    return '{} {} #[{}]{}'.format(cron, cmd, PREFIX, name)

def get_name(line):
    """Get the name of a given line in crontab"""
    global PREFIX
    head = '[{}]'.format(PREFIX)
    if head in line:
        split = line.split(head)
        return split[1]

    return ''

def add_or_replace_cron(head, crontime, command):
    """Add a new line to crontab or replace existing one with same name"""
    cron = CronTab(user=getpass.getuser())

    added = False
    for job in cron:
        #Replace the job here
        if head in job.comment:
            print('Updating existing schedule'.format(head))
            job.setall(crontime)
            job.command = command
            added = True

    #Add to the end
    if not added:
        job = cron.new(command=command, comment=head)
        job.setall(crontime)

    cron.write()

def create_head(name):
    """Create the header to append to each crontab line"""
    global PREFIX
    return '[{}]{}'.format(PREFIX, name)

def cron_unschedule(schedulename):
    """Unschedule a meeting given its schedule name"""
    if schedulename.lower() == 'all':
        head = create_head('')
    else:
        head = create_head(schedulename)

    cron = CronTab(user=getpass.getuser())

    removed = False
    for job in cron:
        if head in job.comment:
            cron.remove(job)
            removed = True

    if not removed:
        print('Schedule not found. Unable to remove'.format(head))

    cron.write()

def cron_schedule(schedulename, crontime, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    """Schedules Zoom calls at certain times according to crontime"""
    global PREFIX
    head = create_head(schedulename)
    path = get_full_path()
    cmd = args_to_cmd(path, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout)

    add_or_replace_cron(head, crontime, cmd)


def day_time_schedule(schedulename, days, time, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    """Converts daytime to crontime and schedules"""
    cron_schedule(schedulename, day_time_to_cron(days, time), id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout)

def list_schedule():
    """List the schedule as is in crontab"""
    cron = CronTab(user=getpass.getuser())

    for job in cron:
        if '[{}]'.format(PREFIX) in job.comment:
            name = job.comment.split('[{}]'.format(PREFIX))[1]
            print('{} scheduled {}'.format(name, job.description(use_24hour_time_format=False)))
