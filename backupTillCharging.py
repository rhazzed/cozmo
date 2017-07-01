#!/usr/bin/env python3
############################################################################
# backupTillCharging.py - Make Cozmo drive straight backwards a little
#                         bit, to try to dock with his charger.
#
# HISTORICAL INFORMATION -
#
#  2017-06-30  msipin  Added this header. Drove a little further each try.
#                      Made Cozmo say whether he found the charger or not.
#                      Used default voice_params settings for Cozmo's voice.
############################################################################

import sys
import asyncio
import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from voice_params import *	# Pickup defaults for Cozmo's voice


def backup(robot, trial):
	'''The core of the drive_to_charger program'''
	
	# If the robot is on the charger, do nothing
	if not robot.is_on_charger:
		# drive backwards a small bit
		robot.drive_straight(distance_mm(-40), speed_mmps(100)).wait_for_completed()

	# show the battery voltage
	print("Current battery voltage: %s" % robot.battery_voltage)

	# see if Cozmo already knows where the charger is
	print("Checking if I am on the charger...")
	robot.set_robot_volume(VOICE_DFLT_VOLUME)
	if robot.is_on_charger:
		print("I am! Yay!")
		robot.set_robot_volume(VOICE_EXCITED_VOLUME)
		robot.say_text("yay!",voice_pitch=VOICE_EXCITED_PITCH,duration_scalar=VOICE_EXCITED_SCALAR).wait_for_completed()
		robot.say_text("I found it!",voice_pitch=VOICE_EXCITED_PITCH,duration_scalar=VOICE_EXCITED_SCALAR).wait_for_completed()
	else:
		print("Nope.. not on the charger =(")
		print("Trying again...")
		trial += 1
		if trial < 4:
			backup(robot, trial)
		else:
			print("I'm getting tired. Giving up =(")
			robot.say_text("I'm getting tired.",voice_pitch=VOICE_DFLT_PITCH,duration_scalar=VOICE_DFLT_SCALAR).wait_for_completed()
			robot.say_text("I give up.",voice_pitch=VOICE_DFLT_PITCH,duration_scalar=VOICE_DFLT_SCALAR).wait_for_completed()


def run(sdk_conn):
	'''The run method runs once the Cozmo SDK is connected.'''
	robot = sdk_conn.wait_for_robot()

	try:
		# register the number of trials
		backup(robot, trial=1)

	except KeyboardInterrupt:
		print("")
		print("Exit requested by user")


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on charger for now
    try:
        cozmo.connect(run)
        #cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
