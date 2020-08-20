from platforms import getPlatform, LINUX, WINDOWS
from dateutil import parser
from crontab import CronTab
import getpass

PREFIX = 'AUTOZOOM'

#Get path of file being executed to know what to call from CRON
def getFullPath():
    return __file__.replace('scheduling', 'autozoom')

#Days will be inputted as 'umtwrfs'
def dayTimeToCron(days, time):
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

#Create the command to run
def argsToCmd(path, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    return '{} "python3 {} join {}"'.format(path.replace('autozoom.py', 'cronLauncher.sh'), path, id) + ' ' + ' '.join([('--name '.format(name) if name else ''), ('--password {}'.format(password) if password else ''), ('--audio' if audio else ''), ('--Video' if video else ''), ('--record' if record else ''), ('--keytimeout {}'.format(keytimeout) if keytimeout else ''), ('--starttimeout {}'.format(starttimeout) if starttimeout else ''), ('--jointimeout {}'.format(jointimeout) if jointimeout else ''), ('--passtimeout {}'.format(passtimeout) if passtimeout else '')])

#Create raw line to add to cron
def createCronLine(name, cron, cmd):
    global PREFIX
    return '{} {} #[{}]{}'.format(cron, cmd, PREFIX, name)

def getName(line):
    global PREFIX
    head = '[{}]'.format(PREFIX)
    if head in line:
        split = line.split(head)
        return split[1]

    return ''

#Check if the crontab already has a name of that schedule
def addOrReplaceCron(head, crontime, command):
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

def createHead(name):
    global PREFIX
    return '[{}]{}'.format(PREFIX, name)

def cronUnschedule(schedulename):
    if schedulename.lower() == 'all':
        head = createHead('')
    else:
       head = createHead(schedulename)

    cron = CronTab(user=getpass.getuser())

    removed = False
    for job in cron:
        if head in job.comment:
            cron.remove(job)
            removed = True

    if not removed:
        print('Schedule not found. Unable to remove'.format(head))

    cron.write()

#Used for scheduling Zoom calls to happen at certain times
def cronSchedule(schedulename, crontime, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    global PREFIX
    head = createHead(schedulename)
    path = getFullPath()
    cmd = argsToCmd(path, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout)

    addOrReplaceCron(head, crontime, cmd)


def dayTimeSchedule(schedulename, days, time, id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout):
    cronSchedule(schedulename, dayTimeToCron(days, time), id, password, audio, video, record, name, keytimeout, starttimeout, jointimeout, passtimeout)

def listSchedule():
    cron = CronTab(user=getpass.getuser())

    for job in cron:
        if '[{}]'.format(PREFIX) in job.comment:
            name = job.comment.split('[{}]'.format(PREFIX))[1]
            print('{} scheduled {}'.format(name, job.description(use_24hour_time_format=False)))
