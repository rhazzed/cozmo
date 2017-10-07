#!/usr/bin/env python3

'''Take Picture

Connect to Cozmo and take a picture
'''

import sys
import cozmo
import base64
import requests
import io
import asyncio
from PIL import Image, ImageDraw
from time import sleep



def analyze_image(image_data, filename):
    '''Process image'''
    #newfile = open('test.jpeg', 'wb')
    newfile = open(filename, 'wb')
    newfile.write(image_data)
    newfile.close()
    return "Ok"

def do_photos(robot: cozmo.robot.Robot):
    '''Get current image from cozmo camera'''
    print("Setting up camera for color pictures...")
    robot.camera.color_image_enabled = True
    robot.camera.image_stream_enabled = True
    sleep(2) # Give camera time to switch to color
    ##for x in range(1, 101):
    for x in range(1, 31):
        do_photo(robot, 'test.%d.jpeg' % (x))


def do_photo(robot: cozmo.robot.Robot, filename):
    # wait for a new camera image to ensure it is captured properly
    print("Waiting for a picture...")
    robot.world.wait_for(cozmo.world.EvtNewCameraImage) # <<< script crawls HERE
    print("Found a picture, capturing the picture.")

    # store the image
    latest_image = robot.world.latest_image.raw_image.convert("YCbCr")
    print("Captured picture. Converting Picture.")

    if latest_image is not None:
        in_mem_file = io.BytesIO()
        latest_image.save(in_mem_file, format = "JPEG")
        # reset file pointer to start
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()
        analyze_image(img_bytes, filename)

        cozmo.logger.info("Success")
        # return image_data
    else:
        cozmo.logger.info("Error")
        print("Error: I have no photo")


def do_say(robot: cozmo.robot.Robot):
    robot.say_text("Hello World").wait_for_completed()

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(do_photos)
