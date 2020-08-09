from platforms import getPlatform, LINUX, WINDOWS
from dateutil import parser
from crontab import CronTab
import getpass

PREFIX = 'AUTOZOOM'

#Get path of file being executed to know what to call from CRON
def getFullPath():
    return __file__

#Days will be inputted as 'umtwrfs'
def dayTimeToCron(days, time):
    days = days.lower()
    for c in days:
        if not c in 'umtwrfs':
            raise Exception('Invalid date string. Must only contain umtwrfs.')

    day_key = list('umtwrfs')
    date = parser.parse(time)
    cron_days = ','.join([str(day_key.index(d) + 1) for d in days])
    minute = date.minute
    hour = date.hour

    return '{} {} * * {}'.format(minute, hour, cron_days)

#Create the command to run
def argsToCmd(path, id, password, audio, video, record, name):
    return 'python3 {} join {}'.format(path, id) + ' '.join([('--name '.format(name) if name else ''), ('--password {}'.format(password) if password else ''), ('--audio' if audio else ''), ('--Video' if video else ''), ('--record' if record else '')])

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
            print('Schedule {} already exists, updating'.format(head))
            job.setall(crontime)
            job.command = command
            added = True

    #Add to the end
    if not added:
        print('Schedule {} doesn\'t exist, creating'.format(head))
        job = cron.new(command=command, comment=head)
        print('Setting time')
        job.setall(crontime)

    cron.write()

def createHead(name):
    global PREFIX
    return '[{}]{}'.format(PREFIX, name)

def cronUnschedule(schedulename):
    head = createHead(schedulename)

    cron = CronTab(user=getpass.getuser())

    removed = False
    for job in cron:
        if head in job.comment:
            print('Removed cronjob {}'.format(head))
            cron.remove(job)
            removed = True

    if not removed:
        print('{} not found. Unable to remove'.format(head))

    cron.write()

#Used for scheduling Zoom calls to happen at certain times
def cronSchedule(schedulename, crontime, id, password, audio, visual, record, name):
    global PREFIX
    head = createHead(schedulename)
    path = getFullPath()
    cmd = argsToCmd(path, id, password, audio, visual, record, name)

    addOrReplaceCron(head, crontime, cmd)


def dayTimeSchedule(schedulename, days, time, id, password, audio, visual, record, name):
    cronSchedule(schedulename, dayTimeToCron(days, time), id, password, audio, visual, record, name)
