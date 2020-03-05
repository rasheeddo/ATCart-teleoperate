#!/bin/bash

gst-launch-1.0 -e -v udpsrc port=23456 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink