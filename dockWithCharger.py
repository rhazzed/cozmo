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


def drive_to_charger(robot, trial):
	'''The core of the drive_to_charger program'''
	
	# If the robot is on the charger, drive forward and clear of the charger
	if robot.is_on_charger:
		# drive off the charger
		print("I am on the charger. Driving off of it...")
		robot.drive_off_charger_contacts().wait_for_completed()
		robot.drive_straight(distance_mm(70), speed_mmps(50)).wait_for_completed()
		# Start moving his arms down
		robot.move_lift(-3)
		# turn around to look at the charger
		robot.turn_in_place(degrees(180)).wait_for_completed()
		# Make his head level
		robot.set_head_angle(degrees(0)).wait_for_completed()
		# wait half a second to ensure Cozmo has seen the charger
		time.sleep(0.5)
		# drive backwards away from the charger
		robot.drive_straight(distance_mm(-60), speed_mmps(50)).wait_for_completed()

	# try to find the charger
	charger = None
	
	# show the battery voltage
	print("Current battery voltage: %s" % robot.battery_voltage)

	# see if Cozmo already knows where the charger is
	if robot.world.charger:
		if robot.world.charger.pose.origin_id == robot.pose.origin_id:
			print("Cozmo already knows where the charger is!")
			charger = robot.world.charger
		else:
			# Cozmo knows about the charger, but the pose is not based on the
			# same origin as the robot (e.g. the robot was moved since seeing
			# the charger) so try to look for the charger first
			pass

	if not charger:
		# Tell Cozmo to look around for the charger
		print("looking for the charger now...")
		look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
		try:
			charger = robot.world.wait_for_observed_charger(timeout=60)
			print("Found charger: %s" % charger)
		except asyncio.TimeoutError:
			print("Didn't see the charger")
		finally:
			# whether we find it or not, we want to stop the behavior
			look_around.stop()

	if charger:
		# lift his arms
		robot.set_lift_height(0.8,0.8,0.8,0.1).wait_for_completed()
		# Attempt to drive near to the charger, and then stop.
		print("Trial number %s" % trial)
		print("Going for the charger!!!")
		#robot.go_to_pose(charger.pose, relative_to_robot=True).wait_for_completed()
		#action = robot.go_to_object(charger, distance_mm(60.0))
		action = robot.go_to_pose(charger.pose)
		action.wait_for_completed()
		print("Completed action: result = %s" % action)
		robot.drive_straight(distance_mm(-30), speed_mmps(50)).wait_for_completed()
		print("Done.")
        
		# Turn 180 (and 10) degrees, then goes backwards at full speed
		print("Now the grand finale: turning around to dock!")
		print("Turning...")
		#robot.turn_in_place(degrees(190)).wait_for_completed()
		robot.turn_in_place(degrees(95)).wait_for_completed()
		robot.turn_in_place(degrees(95)).wait_for_completed()
		#robot.turn_in_place(degrees(10)).wait_for_completed()
		time.sleep( 1 )
		print("Look out: here I go!")
		robot.drive_straight(distance_mm(-130), speed_mmps(150)).wait_for_completed()
		
		print("checking if I did it...")
		if robot.is_on_charger:
			print("I did it! Yay!")
		else:
			print("Nope.. missed the charger =(")
			print("Trying again...")
			robot.world.charger = None
			print("going out further for a better perspective...")
			robot.drive_straight(distance_mm(90), speed_mmps(50)).wait_for_completed()
			trial += 1
			if trial < 4:
				drive_to_charger(robot, trial)
			else:
				print("I'm getting tired. Giving up =(")


def run(sdk_conn):
	'''The run method runs once the Cozmo SDK is connected.'''
	robot = sdk_conn.wait_for_robot()

	try:
		# register the number of trials
		drive_to_charger(robot, trial=1)

	except KeyboardInterrupt:
		print("")
		print("Exit requested by user")


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on charger for now
    try:
        cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
