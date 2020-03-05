#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import socket
import struct
import time
import math as m
import numpy as np
import pygame

######################### constant #########################
minScaler = 1000.0
maxScaler = 2000.0

maxDeadBand = 0.01
minDeadBand = -0.01

maxStick = 1.0
minStick = -1.0
midStick = 0.0

divider = 2.0

maxRPM = 60.0
zeroRPM = 0.0
maxSkidRPM = maxRPM/2.0
#############################################################

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

def DriveWheels(rpmR, rpmL):
    udpPacket = struct.pack('ff', rpmR, rpmL)  # input float values
    moab_sock.sendto(udpPacket, (MOAB_COMPUTER, MOAB_PORT))

def getButton():
	#Read input from the two joysticks
	pygame.event.pump()
	button0 =  j.get_button(0)
	button1 =  j.get_button(1)
	button2 =  j.get_button(2)
	button3 =  j.get_button(3)
	button4 =  j.get_button(4)
	button5 =  j.get_button(5)
	button6 =  j.get_button(6)
	button7 =  j.get_button(7)
	button8 =  j.get_button(8)
	button9 =  j.get_button(9)
	button10 =  j.get_button(10)
	button11 =  j.get_button(11)

	joy_button = [button0, button1, button2, button3, button4, button5, button6, button7,button8, button9, button10, button11]

	return joy_button

def getAxis():
	#Read input from the two joysticks
	pygame.event.pump()
	axis0 =  j.get_axis(0)
	axis1 =  j.get_axis(1)
	axis2 =  j.get_axis(2)
	axis3 =  j.get_axis(3)

	joy_axis = [axis0, axis1, axis2, axis3]
	return joy_axis

def getHat():
	pygame.event.pump()
	hat0 =  j.get_hat(0)
	joy_hat = hat0

	return joy_hat

def map(val, in_min, in_max, out_min, out_max):

	return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def axesTorpm(UD_ch, LR_ch, TW_ch, B1):
	# ax1 is for throttle, UD_ch (up-down channel)
	# ax0 is for curve, LR_ch (left-right channel)
	# ax2 is for skidding, TW_ch (twist channel)

	UD_ch = -UD_ch # flip the sign value

	if B1 == 1:
		###################################### Skidding #######################################
		#((UD_ch <= maxDeadBand) and (UD_ch >= minDeadBand) and ((LR_ch >= maxDeadBand) or (LR_ch <= minDeadBand)) )
		if ((TW_ch >= maxDeadBand) or (TW_ch <= minDeadBand)):
			motorL = map(TW_ch, minStick, maxStick, -maxSkidRPM, maxSkidRPM)
			motorR = -motorL
		else:
			motorR = 0.0
			motorL = 0.0

		print("skidding")
		
	else:
		################################### Straight Drive ###################################
		#if ((LR_ch <= maxDeadBand) and (LR_ch >= minDeadBand) and (UD_ch <= maxDeadBand) and (UD_ch >= minDeadBand)):
		#	motorR = 0.0
		#	motorL = 0.0
		#	print("stop")

		if ( (LR_ch <= maxDeadBand) and (LR_ch >= minDeadBand) and ((UD_ch >= maxDeadBand) or (UD_ch <= minDeadBand))):
			motorR = map(UD_ch, minStick, maxStick, -maxRPM, maxRPM)
			motorL = motorR

			print("straight line")



		####################################### Curves ########################################
		elif( (UD_ch > maxDeadBand) and (LR_ch > maxDeadBand)):
			motorL = map(UD_ch, maxDeadBand+0.01, maxStick, zeroRPM, maxRPM)
			SCALE = map(LR_ch, maxDeadBand+0.01, maxStick, minScaler, maxScaler)
			motorR= motorL*minScaler/SCALE

			print("go up-right")
		
		elif( (UD_ch > maxDeadBand) and (LR_ch < minDeadBand)):
			motorR = map(UD_ch, maxDeadBand+0.01, maxStick, zeroRPM, maxRPM)
			SCALE = map(LR_ch, minDeadBand-0.01, minStick, minScaler, maxScaler)
			motorL = motorR*minScaler/SCALE

			print("go up-left")

		elif( (UD_ch < minDeadBand) and (LR_ch < minDeadBand)):
			motorR = map(UD_ch, minDeadBand-0.01, minStick, zeroRPM, -maxRPM)
			SCALE = map(LR_ch, minDeadBand-0.01, minStick, minScaler, maxScaler)
			motorL = motorR*minScaler/SCALE

			print("go down-left")

		elif( (UD_ch < minDeadBand) and (LR_ch > maxDeadBand)):
			motorL = map(UD_ch, minDeadBand-0.01, minStick, zeroRPM, -maxRPM)
			SCALE = map(LR_ch, maxDeadBand+0.01, maxStick, minScaler, maxScaler)
			motorR = motorL*minScaler/SCALE

			print("go down-right")
		else:
			motorR = 0.0
			motorL = 0.0
			print("else")

	return [motorR, motorL]
	


############################# UDP connection #############################

#moab_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
joy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sbus_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send to MOAB
#MOAB_COMPUTER = "192.168.8.20"
JETSON_NANO = "192.168.8.162"

#MOAB_PORT = 12346
JOY_PORT = 12312

#moab_sock.bind(('0.0.0.0', 0))
joy_sock.bind(('0.0.0.0', JOY_PORT))
#joy_sock.setblocking(0)

#drive_flag_sock.bind((ROBOT_IP, DRIVE_FLAG_PORT))

#drive_flag_sock.setblocking(0)  # set to non-blocking mode
rpmR = 0.0
rpmL = 0.0
while True:
	Axes = getAxis()
	Buttons = getButton()

	ax0 = Axes[0]
	ax1 = Axes[1]
	ax2 = Axes[2]

	B0 = Buttons[0]
	B1 = Buttons[1]

	if B0 == 1:
		rpmR, rpmL = axesTorpm(ax1, ax0, ax2, B1)
		rpmPacket = struct.pack('ff',rpmR, rpmL)
		joy_sock.sendto(rpmPacket,(JETSON_NANO, JOY_PORT))
	else:
		rpmPacket = struct.pack('ff',0.0, 0.0)
		joy_sock.sendto(rpmPacket,(JETSON_NANO, JOY_PORT))

	#DriveWheels(rpmR, rpmL)
	#print("rpmR: " + "{:.4f}".format(rpmR) + "  rpmL: " + "{:.4f}".format(rpmL))
	#print("rpmL", rpmL)