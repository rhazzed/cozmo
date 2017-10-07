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



def analyze_image(image_data):
    '''Process image'''
    newfile = open('test.png', 'wb')
    newfile.write(image_data)
    newfile.close()
    return "Ok"

def do_photo(robot: cozmo.robot.Robot):
    '''Get current image from cozmo camera'''
    print("Waiting for a picture...")
    robot.camera.color_image_enabled = True
    robot.camera.image_stream_enabled = True


    # wait for a new camera image to ensure it is captured properly
    robot.world.wait_for(cozmo.world.EvtNewCameraImage) # <<< script crawls HERE
    print("Found a picture, capturing the picture.")

    # store the image
    latest_image = robot.world.latest_image.raw_image.convert("RGB")
    print("Captured picture. Converting Picture.")

    if latest_image is not None:
        in_mem_file = io.BytesIO()
        latest_image.save(in_mem_file, format = "PNG")
        # reset file pointer to start
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()
        #image_64_encode = base64.b64encode(img_bytes)
        #image_data = 'data:image/jpeg;base64,'+image_64_encode.decode("utf-8")
        #analyze_image(image_data)
        analyze_image(img_bytes)
        cozmo.logger.info("Success")
        # return image_data
    else:
        cozmo.logger.info("Error")
        return "Error: I have no photos"

def do_say(robot: cozmo.robot.Robot):
    robot.say_text("Hello World").wait_for_completed()

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(do_photo)
