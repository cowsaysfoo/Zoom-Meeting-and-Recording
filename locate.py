import os
from subprocess import PIPE, Popen
import pyautogui

resolutions = []

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0].decode('utf-8')

def getResolutions():
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
   
    return ['{}/{}.png'.format(res, name) for res in resolutions]
    

#Search through all screens
def locate(name):
    paths = resolveName(name)

    for path in paths:
        result =  pyautogui.locateCenterOnScreen(path, confidence=0.5)

        if result:
            return result

    return None
