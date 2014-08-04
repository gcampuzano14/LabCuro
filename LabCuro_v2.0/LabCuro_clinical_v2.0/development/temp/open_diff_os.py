import subprocess
import sys

def openFolder(path):
    if sys.platform == 'darwin':   
        subprocess.call(['open', path])
    elif sys.platform == 'linux2':
        subprocess.call(['gnome-open', '--', path])
    elif sys.platform == 'win32':
        subprocess.call(['explorer', path])
    return sys.platform
