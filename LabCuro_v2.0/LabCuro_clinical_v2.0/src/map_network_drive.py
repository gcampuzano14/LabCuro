import win32api
import win32net
import os
import string
import subprocess
import re
import socket






def map_netdrive(netdrive, domain, username, password):
    server_addr = re.match(r'\\\\(.+?)(\\.*)',netdrive)
    server_ip = server_addr.group(1)
    client = socket.gethostbyname_ex( server_ip )[2][0]
    sharedrive = '\\\\'+client+server_addr.group(2)
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
    cmd_parts = ["NET USE %s: %s" % (availletter[0], sharedrive)]  # uses first letter available to map drive
    test = subprocess.call(" ".join(cmd_parts))

    if test==0:
        networkdrive_letter = availletter[0]
        return networkdrive_letter
    else:
        pass

    cmd_parts = ["NET USE %s: %s" % (availletter[0], sharedrive) , password, "/USER:%s\%s" % (domain, username)]  # uses first letter available to map drive
    test = subprocess.call(" ".join(cmd_parts))  # t = 0 is successful connection

    if test==0:
        networkdrive_letter = availletter[0]
        return networkdrive_letter
    else:
        print 'error'
        quit()

    
def mapped_drives(net_drive_paths):
    
    drives = win32net.NetUseEnum(None,0)
    drives_to_unmap = []
    for e in net_drive_paths:
        server_addr = re.match(r'\\\\(.+?)(\\.*)',e)
        server_ip = server_addr.group(1)
        
        client = socket.gethostbyname_ex( server_ip )
        drives_to_unmap.append(e)
        ip_map_list = [str('\\\\'+x+server_addr.group(2)) for x in client[2]]
        drives_to_unmap = ip_map_list + drives_to_unmap
    print drives_to_unmap    
    for e in drives_to_unmap:
        #print e
        for drive in drives[0]:
           # print drive
            if e.lower() == drive['remote'].lower():
                os.system(r"NET USE %s: /DELETE /YES" % drive['local'][0])   