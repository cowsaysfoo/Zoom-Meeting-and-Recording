import time
import os
import pyautogui
import locate
from platforms import getPlatform, LINUX, WINDOWS

def restart_zoom():
    """Closes then re-opens Zoom process"""
    print('Restarting')
    if getPlatform() == LINUX:
        os.system("ps aux | grep zoom | grep autozoom -v |  awk '{print $2}' | xargs kill")
        time.sleep(1)
        os.system('/usr/bin/zoom &')
    elif getPlatform() == WINDOWS:
        os.system("for /f \"tokens=2\" %A in ('tasklist ^| findstr /i \"Zoom\" 2^>NUL') do taskkill /F /PID %A")
        time.sleep(1)
        os.startfile(os.getenv('APPDATA') + '\\Zoom\\bin\\Zoom.exe')
    else:
        print('Error: Unsupported operating system: {}. Please submit an issue'.format(getPlatform()))
        exit(1)

def connect(meet_id, password, audio, video, name, fixdropdown, keytimeout, starttimeout, jointimeout, passtimeout):
    """Connect to meeting with the options above"""
    #We need to inverse it so it doesn't kill the current process
    restart_zoom()
    time.sleep(starttimeout)

    x, y = locate.locate('btnJoin')
    pyautogui.click(x, y)
    time.sleep(jointimeout)

    #Enter meeting id
    x, y = locate.locate('txtId')
    pyautogui.click(x, y)
    time.sleep(keytimeout)
    pyautogui.write(meet_id)
    time.sleep(keytimeout)

    #This is for if the V is not there, users must manually tell it
    if not fixdropdown:
        pyautogui.press('tab', interval=0.5)
    pyautogui.press('tab', interval=0.5)

    if name:
        pyautogui.press('backspace', 50)
        pyautogui.write(name)

    pyautogui.press('tab', interval=0.5)

    #Set audio enable
    if not audio:
        pyautogui.press('enter', interval=0.5)

    pyautogui.press('tab', interval=0.5)

    #Set video enable
    if not video:
        pyautogui.press('enter', interval=0.5)

    #Navigate to the next screen
    pyautogui.press('tab', interval=0.5)
    pyautogui.press('enter', interval=1)

    #Password
    if password:
        time.sleep(passtimeout)

        #Check for error message
        result = locate.locate('errorid')

        #If there is an error message, remove it
        if result:
            x, y = locate.locate('btnLeave')
            pyautogui.click(x, y)
            time.sleep(keytimeout)

        result = locate.locate('txtPass')

        #If the error was actuall fake, and password thing is there, enter the password
        if result:
            x, y = result
            pyautogui.click(x, y)
            time.sleep(keytimeout)
            pyautogui.write(password)
            time.sleep(keytimeout)

            pyautogui.press('tab', interval=0.5)
            pyautogui.press('enter', interval=1)
        else:
            print('Fatal error occured. Invalid meeting id.')
