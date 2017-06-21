#!/usr/bin/env python3

# Read and display Cozmo's current battery voltage.

import sys
import asyncio
import time
import cozmo


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
