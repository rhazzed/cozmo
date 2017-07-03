#!/usr/bin/env python3
############################################################################
# readbatteryvoltage.py - Read and display Cozmo's current battery voltage.
#
# HISTORICAL INFORMATION -
#
#  2017-07-02  msipin  Added this header. Added ability to only display
#                      the percent full with a "-f" ("full") command-line
#                      parameter.
############################################################################

import sys
import asyncio
import time
import cozmo

# On Charger -  (Anything greater than 4.40)
# 100% full -   Current battery voltage: 4.0799560546875
# 75% full -    Current battery voltage: 3.85595703125
# 50% full -    Current battery voltage: 3.72796630859375
# 25% full -    Current battery voltage: 3.62799072265625
# ALMOST DEAD - Current battery voltage: 3.48797607421875
# DEAD -        Current battery voltage: 3.43194580078125

# Presumed "linear" region -
FULL_BATT = 4.100000
AD_BATT   = 3.550000

pct_full_only=False

def showVoltage(robot):

    bv = robot.battery_voltage
    truncVal = float('%.f' % float(bv/FULL_BATT*100.0))

    if pct_full_only:
        print("{0}".format(truncVal))
    else:
        # show the battery voltage
        print("Current battery voltage: %s" % bv)
        if bv > FULL_BATT:
            print("Probably on charger")
        elif bv > AD_BATT:
            print("Estimated: {0}% full".format(truncVal))
        else:
            print("**** Need to recharge! ****   ALMOST DEAD!   (Only a few minutes left!)")


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

    if (len(sys.argv)>1 and "-f" == sys.argv[1]):
        pct_full_only=True

    try:
        # Connect WITHOUT displaying what Cozmo sees -
        cozmo.connect(run)
        # Connect and show what Cozmo sees -
        #cozmo.connect_with_tkviewer(run, force_on_top=True)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
