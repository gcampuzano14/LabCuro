import socket
import win32api
import win32net
import os
import string
import subprocess
import sys




t=getattr(sys, 'path')[0]
print t
#server_addr = 'jhscel01.um-jmh.org'
#server_addr = 'cgcent.miami.edu'
server_addr ='protocz'
#non_open_port = 90
client = socket.gethostbyname_ex( server_addr )
#client = socket.gethostbyname_ex( client[2][0] )
#print emote_ip
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.connect((server_addr, non_open_port))
#client = s.getsockname()[0]
print client
print str('\\\\'+ client[2][0] + '\\DEPTSHARE\\Pathology-Clinical-Flow-Cytometry\\LABCURO_V2.0')


#cmd_parts = ["NET USE %s: %s" % ('a', str('\\\\'+ client[2][0] + '\\DEPTSHARE\\Pathology-Clinical-Flow-Cytometry\\LABCURO_V2.0') )]  # uses first letter available to map drive
#test = subprocess.call(" ".join(cmd_parts)) 
#server_addr = 'jhscel01.um-jmh.org'
#non_open_port = 90

#client = socket.gethostbyname_ex( server_addr )
#print client
#cmd_parts = ["NET USE %s: %s" % ('b', str('\\\\'+ client[2][0] + '\\JMH_Flow_Cytometry\\LABCURO_V2.0') ), '1236.Gcz', "/USER:%s\%s" % ('MEDICAL', 'gcampuzanozuluaga')]  # uses first letter available to map drive
#print cmd_parts
#cmd_parts = ["NET USE %s: %s" % ('b', str('\\\\'+ client[2][0] + '\\german_share\labcurotest_1\LABCURO_V2.0') ), 'cAmpzUlu52', "/USER:%s\%s" % ('protocz', 'gcampuzano')]
cmd_parts = ["NET USE %s: %s" % ('b', str('\\\\'+ client[2][0] + '\\german_share\\labcurotest_1\\LABCURO_V2.0') )]

test = subprocess.call(" ".join(cmd_parts)) 
print test
