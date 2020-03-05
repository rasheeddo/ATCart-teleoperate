#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import socket
import struct
import time
import math as m
import numpy as np

############################# UDP connection #############################

moab_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
joy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sbus_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send to MOAB
MOAB_COMPUTER = "192.168.8.20"
#TELE_COMPUTER = "192.168.8.181"

MOAB_PORT = 12346
JOY_PORT = 12312

moab_sock.bind(('0.0.0.0', 0))
joy_sock.bind(('0.0.0.0', JOY_PORT))
joy_sock.setblocking(0)

def DriveWheels(rpmR, rpmL):
	udpPacket = struct.pack('ff', rpmR, rpmL)  # input float values
	moab_sock.sendto(udpPacket, (MOAB_COMPUTER, MOAB_PORT))

DriveWheels(0.0, 0.0)
print("					wait a sec to start....")
print("					switch ch5 to auto-mode")
time.sleep(1.0)

rpm_R = 0.0
rpm_L = 0.0

while True:

	try:
		data, addr = joy_sock.recvfrom(1024)
		rpm_R, rpm_L = struct.unpack('ff',data)
	except socket.error:
		#rpm_R = 0.0
		#rpm_L = 0.0
		pass

	print("rpmR: " + "{:.4f}".format(rpm_R) + "  rpmL: " + "{:.4f}".format(rpm_L))
	DriveWheels(rpm_R, rpm_L)


