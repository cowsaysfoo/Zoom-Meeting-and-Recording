import platform

PLATFORM = 0

LINUX = 1
WINDOWS = 2

def getPlatform():
    global PLATFORM

    if PLATFORM == 0:
        if 'linux' in platform.platform().lower():
            PLATFORM = LINUX
        elif 'windows' in platform.platform().lower():
            PLATFORM = WINDOWS
    
    return PLATFORM
