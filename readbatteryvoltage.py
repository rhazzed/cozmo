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

'''Make Cozmo drive to his charger.
'''

import sys
import asyncio
import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps


def showVoltage(robot):
	# show the battery voltage
	print("Current battery voltage: %s" % robot.battery_voltage)


def run(sdk_conn):
	'''The run method runs once the Cozmo SDK is connected.'''
	robot = sdk_conn.wait_for_robot()

	try:
		showVoltage(robot)

	except KeyboardInterrupt:
		print("")
		print("Exit requested by user")


if __name__ == '__main__':
    #cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on charger for now

    try:
        # Connect WITHOUT displaying what Cozmo sees -
        cozmo.connect(run)
        # Connect and show what Cozmo sees -
        #cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
