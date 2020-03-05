#!/usr/bin/env python3

import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

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

while True:
	Buttons = getButton()
	Axes = getAxis()
	Hat = getHat()

	print("Buttons", Buttons)
	print("Axes", Axes)
	print("Hat", Hat)

