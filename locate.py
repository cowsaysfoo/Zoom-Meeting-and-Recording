import os
from subprocess import PIPE, Popen
import pyautogui
import platform

if 'windows' in platform.platform().lower():
    from screeninfo import get_monitors

resolutions = []

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0].decode('utf-8')

def getResolutions():
    plat = platform.platform().lower()

    if 'linux' in plat:
       return getResolutionsLinux()
    elif 'windows' in plat:
        return getResolutionsWindows()
    else:
        print('Error: Unsupported operating system: {}. Please submit an issue'.format(plat))
        exit(1)


def getResolutionsWindows():
    return ['{}x{}'.format(m.width, m.height) for m in get_monitors()]

def getResolutionsLinux():
        results = cmdline('xrandr | grep -E "[[:digit:]]+x[[:digit:]]+\+" -o | sed "s/\+//g"')
        results = results.strip().split('\n')

        exists = []
        for res in results:
            if not os.path.isdir(res):
                print('Resolution {} is not supported. Please submit an issue'.format(res))
                exists.append(False)
            else:
                exists.append(True)

        if sum(exists) == 0:
            print('Error: No supported resolutions.')
            exit()

        return [res for (res, exist) in zip(results, exists) if exist]

def resolveName(name):
    global resolutions
    if len(resolutions) == 0:
        resolutions = getResolutions()
   
    if 'windows' in platform.platform().lower():
        return ['{}windows/{}.png'.format(res, name) for res in resolutions]
    else:
        return ['{}/{}.png'.format(res, name) for res in resolutions]

#Search through all screens
def locate(name):
    paths = resolveName(name)

    for path in paths:
        print('Using ', path)
        result =  pyautogui.locateCenterOnScreen(path, confidence=0.5)

        if result:
            return result

    return None
