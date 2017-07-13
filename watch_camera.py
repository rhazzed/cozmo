#!/usr/bin/env python3
# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

''' watch_camera.py

Watch Cozmo's video feed

'''

import sys
import cozmo
import asyncio
from time import sleep
from threading import Thread
import cozmo
from PIL import Image, ImageDraw

counter=0
last_counter=0


# Annotator for displaying RobotState (position, etc.) on top of the camera feed
class RobotStateDisplay(cozmo.annotate.Annotator):
    def apply(self, image, scale):
        global counter


        counter += 1
        d = ImageDraw.Draw(image)

        bounds = [3, 0, image.width, image.height]

        def print_line(text_line):
            text = cozmo.annotate.ImageText(text_line, position=cozmo.annotate.TOP_LEFT, color='lightblue')
            text.render(d, bounds)
            TEXT_HEIGHT = 11
            bounds[1] += TEXT_HEIGHT

        robot = self.world.robot

        # Display the Pose info for the robot

        pose = robot.pose
        print_line('Pose: Pos = <%.1f, %.1f, %.1f>' % pose.position.x_y_z)
        print_line('Pose: Rot quat = <%.1f, %.1f, %.1f, %.1f>' % pose.rotation.q0_q1_q2_q3)
        print_line('Pose: angle_z = %.1f' % pose.rotation.angle_z.degrees)
        print_line('Pose: origin_id: %s' % pose.origin_id)

        # Display the Accelerometer and Gyro data for the robot

        print_line('Accelmtr: <%.1f, %.1f, %.1f>' % robot.accelerometer.x_y_z)
        print_line('Gyro: <%.1f, %.1f, %.1f>' % robot.gyro.x_y_z)



def run(sdk_conn):
    '''The run method runs once Cozmo is connected.'''

    foundIt=0
    sayThis = ""

    robot = sdk_conn.wait_for_robot()
    robot.world.image_annotator.add_annotator('robotState', RobotStateDisplay)
    print
    input("Press <Enter> when you wish to exit this program...")
    print

    

if __name__ == '__main__':
    cozmo.robot.Robot.drive_off_charger_on_connect = True


    def _call_me(arg1, arg2):
        global counter
        global last_counter

        while True:
            print("Loop counter: {0} (FPS: {1})".format(counter,counter-last_counter))
            last_counter = counter
            sleep(1)

    thread = Thread(target=_call_me,
                    kwargs=dict(arg1="Hello", arg2="There"))
    thread.daemon = True # Force to quit on main quitting
    thread.start()




    try:
            cozmo.setup_basic_logging()
            cozmo.connect_with_tkviewer(run, force_on_top=False)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
