#!/usr/bin/env python3
############################################################################
# time2words.py - A program to display the current time as words (e.g.
#                 09:31:00 = "Nine thirty one AM"
#
# HISTORICAL INFORMATION -
#
#  2017-07-02  msipin  Inspired by the great Physics Denier, Eric P.
#                      Added ability to skip speaking the seconds with "-m"
#                      ("minutes") command-line parameter.
############################################################################

import sys
import time
import datetime

num2words = {1: 'One ', 2: 'Two ', 3: 'Three ', 4: 'Four ', 5: 'Five ', \
             6: 'Six ', 7: 'Seven ', 8: 'Eight ', 9: 'Nine ', 10: 'Ten ', \
            11: 'Eleven ', 12: 'Twelve ', 13: 'Thirteen ', 14: 'Fourteen ', \
            15: 'Fifteen ', 16: 'Sixteen ', 17: 'Seventeen ', 18: 'Eighteen ', \
            19: 'Nineteen ', 20: 'Twenty ', 30: 'Thirty ', 40: 'Forty ', \
            50: 'Fifty ', 60: 'Sixty ', 70: 'Seventy ', 80: 'Eighty ', \
            90: 'Ninety ', 0: 'Oh '}

def n2w(n):
    try:
        sys.stdout.write(num2words[n])
    except KeyError:
        try:
            sys.stdout.write(num2words[n-n%10] + " " +num2words[n%10].lower())
        except KeyError:
            sys.stdout.write('Number out of range')

def main(argv):
    # Main function
    skip_seconds=False

    if (len(sys.argv)>1 and "-m" == sys.argv[1]):
        skip_seconds=True

    # Get current time
    now=datetime.datetime.now()
    currTime=now.strftime("%H:%M:%S")
    #currTime="08:34:21"
    sys.stdout.write("Current time: {0}\n".format(currTime))

    # Split time by colons
    EA=currTime.split(":")

    # Convert each colon into "number string"

    # Deal with AM/PM
    isAM=1
    if (int(EA[0]) > 11):
        isAM=0
    if (int(EA[0]) > 12):
        EA[0] = int(EA[0]) - 12

    # Hours
    if (int(EA[0]) == 0):
        EA[0] = int(EA[0]) + 12

    n2w(int(format(EA[0])))

    # If user wants to skip seconds, just set to zero and let
    # logic below handle it
    if skip_seconds:
        EA[2] = "00"

    # If both minutes and seconds are zero, don't show them
    if (int(EA[1]) != 0 or int(EA[2]) != 0):
        # Minutes
        if (int(EA[1]) < 10):
            if (int(EA[1]) != 0):
                sys.stdout.write("Oh ")
        n2w(int(format(EA[1])))

        # If seconds are zero, don't show them
        if (int(EA[2]) != 0):
            # Seconds
            if (int(EA[2]) < 10):
                if (int(EA[2]) != 0):
                    sys.stdout.write("Oh ")
            n2w(int(format(EA[2])))

    # AM/PM
    if (isAM):
        sys.stdout.write("AM")
    else:
        sys.stdout.write("PM")

    sys.stdout.write("\n")

if __name__=='__main__':
    sys.exit(main(sys.argv))
