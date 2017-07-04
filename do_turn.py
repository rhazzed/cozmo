#!/usr/bin/env python3
############################################################################
# do_drive.py - Make Cozmo drive straight (forwards or backwards) as far as
#               the user specified on the command line.
#
# HISTORICAL INFORMATION -
#
#  2017-07-03  msipin  Derived from backupTillCharging.py
#  2017-07-04  msipin  Set Cozmo to stay on the charger if he's already
#                      there. (The default "drive off the charger" behavior
#                      does not adequately clear the charger to allow him
#                      to safely turn thereafter.)
############################################################################

import sys
import asyncio
import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose


def usage():
	print("\nusage: {0} <degrees>\n".format(sys.argv[0]))
	print("       Clockwise is positive degrees, anti-clockwise is negative\n")

def turn_deg(robot,num_degrees):
	'''The core of the program'''

	###############
	# My robot is off from a cold start by a few degrees
	###############
	adjustment_factor = 0.000	# Default to none
	leftover_degrees = 0.00

	if (num_degrees > 0.00):	# Clockwise -
		adjustment_factor = 1.0200	# % error
	else:				# Anti-clockwise -
		adjustment_factor = 1.0219	# % error

	corrected_num_degrees = num_degrees * adjustment_factor

	if corrected_num_degrees > 360.0:
		leftover_degrees = corrected_num_degrees - 360.0
	if corrected_num_degrees < -360.0:
		leftover_degrees = corrected_num_degrees + 360.0

	# If the robot is on the charger, do nothing
	if robot.is_on_charger:
		# Don't do it...
		print("Can not turn - I am on the charger!")
	else:
		robot.turn_in_place(degrees(num_degrees*-1.0)).wait_for_completed()	# Positive = CLOCKWISE
		if leftover_degrees != 0.00:
			robot.turn_in_place(degrees(leftover_degrees*-1.0)).wait_for_completed()


def run(sdk_conn):
	'''The run method runs once the Cozmo SDK is connected.'''
	robot = sdk_conn.wait_for_robot()

	try:
		# Pickup user-provided degrees
		user_deg = float(sys.argv[1])
		print("DEBUG: user_deg = {0}\n".format(user_deg))

		#turn_deg(robot, 90.0) # Turn clockwise some degrees
		#turn_deg(robot, -90.0) # Turn anti-clockwise some degrees
		turn_deg(robot, user_deg)  # Turn as far clockwise/anti-clockwise as user specified

	except KeyboardInterrupt:
		print("")
		print("Interrupted by user")


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = False # Coz should stay on the charger, if he's there


    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    try:
        cozmo.connect(run)
        #cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
