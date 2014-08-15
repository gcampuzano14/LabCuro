import win32api
import win32net
import os
import string
import subprocess
import re
import socket


def map_netdrive(netdrive, domain, username, password):
    
    
    
    
    
    letters = list(string.ascii_uppercase)
    driveletter = []
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        print drive
        drive = drive[0]
        driveletter.append(drive[0])
    availletter = list(set(letters) - set(driveletter))
    #Context manager that mounts the given share using the given username and password to the given drive letter when entering the context and unmounts it when exiting
    cmd_parts = ["NET USE %s: %s" % (availletter[0], netdrive) , password, "/USER:%s\%s" % (domain, username)]  # uses first letter available to map drive
    print cmd_parts
    test = subprocess.call(" ".join(cmd_parts))  # t = 0 is successful connection
    #print " ".join(cmd_parts)
    if test == 0:
        networkdrive_letter = availletter[0]
        return networkdrive_letter
    else:
        print 'error'
        quit()
#def get_ips(shares):
    
 #   for e in shares: 
        
    
    
    
def mapped_drives(net_drive_paths):
    drives = win32net.NetUseEnum(None,0)
    
    for e in net_drive_paths:
        print e
        for drive in drives[0]:
            if e.lower() == drive['remote'].lower():
                os.system(r"NET USE %s: /DELETE /YES" % drive['local'][0])   