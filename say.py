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

''' say.py

Make Cozmo say whatever you type on the command line or input after
starting the program.

'''

import sys
import cozmo
import asyncio
import time
import cozmo
from voice_params import *	# Pickup defaults for Cozmo's voice

def run(sdk_conn):
    '''The run method runs once Cozmo is connected.'''

    foundIt=0
    sayThis = ""

    robot = sdk_conn.wait_for_robot()
    if len(sys.argv)>1:
        for x in sys.argv:
            if (str.endswith(x,"say.py")):
                foundIt = 1
                continue
            if (foundIt == 1):
                sayThis += " "
                sayThis += x
    else:
        print
        sayThis = input("What would you like me to say? : ")
    
    robot.set_robot_volume(VOICE_DFLT_VOLUME)
    robot.say_text(sayThis,voice_pitch=VOICE_DFLT_PITCH,duration_scalar=VOICE_DFLT_SCALAR).wait_for_completed()

if __name__ == '__main__':
    cozmo.robot.Robot.drive_off_charger_on_connect = False  # Don't make Cozmo drive off the charger

    try:
        # If user didn't tell us what to say, start camera and watch as they type
        # If user *did* tell us to say, just say it (without camera)
        if len(sys.argv)>1:
            cozmo.connect(run)
        else:
            cozmo.setup_basic_logging()
            cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
