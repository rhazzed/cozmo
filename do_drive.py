#!/usr/bin/env python3
############################################################################
# do_drive.py - Make Cozmo drive straight (forwards or backwards) as far as
#               the user specified on the command line.
#
# HISTORICAL INFORMATION -
#
#  2017-07-03  msipin  Derived from backupTillCharging.py
############################################################################

import sys
import asyncio
import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from voice_params import *	# Pickup defaults for Cozmo's voice


def usage():
	print("\nusage: {0} <distance_in_inches>\n".format(sys.argv[0]))
	print("       Forward is positive inches, backwards negative\n")

def drive_mm(robot,distance_in_mm):
	'''The core of the drive program'''

	###############
	# My robot is off from a cold start by 1/8 inch per 25.4 mm (forward) and
	# a "somewhat" less than that going backwards... (scientific, no? LOL)
	###############
	adjustment_factor = 0.000	# Default to none
	if (distance_in_mm > 0.00):	# Forward A.F. -
		adjustment_factor = 1.600	# May have to change per robot....YMMV...
	else:				# Reverse A.F. -
		adjustment_factor = 2.550	# May have to change per robot....YMMV...
	corrected_distance_in_mm = distance_in_mm - (distance_in_mm/25.4 * adjustment_factor)
	
	# If the robot is on the charger, and user wants to backup, do nothing
	if robot.is_on_charger and corrected_distance_in_mm < 0:
		# Don't do it...
		print("Can not drive backwards - I am on the charger!")

	else:
		robot.drive_straight(distance_mm(corrected_distance_in_mm), speed_mmps(150)).wait_for_completed()

def run(sdk_conn):
	'''The run method runs once the Cozmo SDK is connected.'''
	robot = sdk_conn.wait_for_robot()

	try:
		# Convert user-provided distance (in inches) to mm
		user_mm = float(sys.argv[1])*25.4
		print("DEBUG: user_mm = {0}\n".format(user_mm))

		#drive_mm(robot, 25.4*3) # Go forward some inches
		#drive_mm(robot, -25.4*3) # Go backwards some inches
		drive_mm(robot, user_mm)  # Go as far forwards/backwards as user specified

	except KeyboardInterrupt:
		print("")
		print("Interrupted by user")


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = True # Coz should drive off the charger, if needed


    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    try:
        cozmo.connect(run)
        #cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
