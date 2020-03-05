#!/bin/bash

gst-launch-1.0 -v v4l2src device=/dev/video0 ! "image/jpeg,width=848, height=480,framerate=30/1" ! rtpjpegpay ! udpsink host=192.168.8.181 port=23456