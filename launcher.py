#!/usr/bin/env python3
############################################################################
# launcher.py - This program is a test of calling other Python programs
#
# HISTORICAL INFORMATION -
#
#  2017-06-30  msipin  Created.
############################################################################

import sys
import asyncio
import time
import cozmo


def doit(var):
    print("Calling '{0}'...".format(var))
    try:
        # Dynamically import the module named by the caller
        mod = __import__(var)
        cozmo.connect(mod.run)
        time.sleep(0.5)
    except ImportError:
        print("\nERROR: [{0}] is not a python module name.".format(var))
        pass


def main(argv):
    # Main function
    print("\nHowdy, this is our main program.")

    cozmo.robot.Robot.drive_off_charger_on_connect = False  # Don't make Cozmo drive off the charger

    print("")
    doit("readbatteryvoltage")
    print("")
    doit("say")
    print("")
    doit("readbatteryvoltage")

    # Let user launch an arbitrary python program -
    print("")
    user_input = input("What Python program would you like to launch (no '.py', command-line arguments ok)? : ")
    # Split input by whitespace
    words = user_input.split()
    # What-to-launch is first
    launchThis = words[0]
    # Clear out existing argv[]
    del sys.argv[:]
    # Append program as first element
    sys.argv.append(launchThis+".py")
    # Argv[] args are next
    for i in range(1,len(words)):
        try:
            sys.argv[i] = words[i]
        except IndexError:
            # This arg doesn't exist. Append it
            sys.argv.append(words[i])
    doit(launchThis)

    time.sleep(1)
    print("\nGoodbye!\n")


if __name__=='__main__':
    sys.exit(main(sys.argv))
