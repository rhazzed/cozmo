#!/usr/bin/env python3
############################################################################
# starfield.py - Draw a "moving starfield" on Cozmo's display
#
# HISTORICAL INFORMATION -
#
#  2017-06-30  msipin  Added this header. Manually handled driving off/
#                      returning to the charger.
############################################################################

import sys
import time
from cozmo.util import distance_mm, speed_mmps

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo
from random import randrange

shouldContinue=1

class starfield:

    def __init__(self, num_stars, max_depth, my_coz):
    	self.coz = my_coz
    	self.clock = time.clock()
    	self.num_stars = num_stars
    	self.max_depth = max_depth
    	self.screen_width = 128
    	self.screen_height = 32
    	self.screen = []
    	
    	for i in range(0, self.screen_width):
    		temp_list = []
    		for j in range(0, self.screen_height):
    			temp_list.append(0x00)
    		self.screen.append(temp_list)
    	self.init_stars()
    	
    def blank_screen(self):
    	for i in range(0, self.screen_width):
    		temp_list = self.screen[i]
    		for j in range(0, self.screen_height):
    			temp_list[j] = 0x00

    def init_stars(self):
        """ Create the starfield """
        self.stars = []
        for i in range(self.num_stars):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self.max_depth)]
            self.stars.append(star)
            
    
    def move_and_draw_stars(self):
        """ Move and draw the stars """
        origin_x = self.screen_width / 2
        origin_y = self.screen_height / 2
        
        self.blank_screen()
        
        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.2
 
            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self.max_depth
 
            # Convert the 3D coordinates to 2D using perspective projection.
            k = 64.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)
 
            # Draw the star (if it is visible in the screen).
            if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
            	row_target = self.screen[x]
            	row_target[y] = 0x01
		
		#transform the screen to a list to be converted into bytes
        newScreen = []
        for i in range(0,self.screen_height):
        	for j in range(0,self.screen_width):
        		newScreen.append((self.screen[j])[i])
		#convert the screen to bytes and send to OLED
        face_image = bytes(newScreen)
        image = cozmo.oled_face.convert_pixels_to_screen_data(face_image,self.screen_width,self.screen_height)
        self.coz.display_oled_face_image(image, 1.0)

    def run(self):
        """ Main Loop """
        global shouldContinue
        while shouldContinue:
        	t0 = time.clock()
        	#throttle the speed of the animation by counting ticks
        	if t0 - self.clock > .01: 
        		self.move_and_draw_stars()
        		self.clock = time.clock()
        # Don't exit this method right away - give
        # Coz enough time to backup into the charger
        # if that's where he was before we started
        time.sleep(10)
           		
def run(sdk_conn):
    '''The run method runs once Cozmo is connected.'''
    global shouldContinue
    robot = sdk_conn.wait_for_robot()

    wasOnCharger = 0

    # If the robot is on the charger, drive forward and clear of the charger
    if robot.is_on_charger:
        wasOnCharger = 1
        # drive off the charger
        robot.drive_off_charger_contacts().wait_for_completed()
        robot.drive_straight(distance_mm(20), speed_mmps(50)).wait_for_completed()

    # move head and lift to make it easy to see Cozmo's face
    robot.set_lift_height(0.0).wait_for_completed()
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    try:
        starfield(300, 32, robot).run()
    except KeyboardInterrupt:
        print("User abort...")
        shouldContinue = 0
        # Give animation a chance to finish at least one redraw
        time.sleep(2)
        pass

    # If we drove him off the charger, drive him back on it
    if wasOnCharger:
        # Backup
        robot.drive_straight(distance_mm(-30), speed_mmps(100)).wait_for_completed()
        if robot.is_on_charger:
            print("Yay! Back on the charger.")
        else:
            print("Nope.. I missed the charger =(")


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    cozmo.robot.Robot.drive_off_charger_on_connect = False
    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)

