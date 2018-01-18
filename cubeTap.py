#!/usr/bin/env python3

# Copyright (c) 2017 Anki, Inc.
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

'''Tell Cozmo to roll a cube that is placed in front of him.

This example demonstrates Cozmo driving to and rolling a cube.
You must place a cube in front of Cozmo so that he can see it.
'''

import cozmo
import concurrent.futures

# Array of cube object ID's (random order)
stuff = []
allFound = False


async def watch_cubes(robot: cozmo.robot.Robot):
	global allFound
	global stuff

	print("Cozmo is waiting for cubes to be tapped")

	while(True):
		try:
			evt = await robot.world.wait_for(cozmo.objects.EvtObjectTapped)
			cube = evt.obj
			#print(evt)
			print("\nCube %d tapped %d time(s), intensity: %d, duration: %d, Visible: %s" % (cube.object_id, evt.tap_count, evt.tap_intensity, evt.tap_duration, cube.is_visible))

			# Pickup cube's "object ID"
			cn = cube.object_id

			# If not seen before, assign this cube's object ID to next available "cube[x]"
			if cube not in stuff:
				# Add cn to list
				stuff.append(cube)
				# Light up the cube
				cube.set_lights(cozmo.lights.green_light)


			# If detected three different cube object ID's, tell user
			if len(stuff) == 3 and allFound == False:
				print("\n\tAll %d cubes detected!\n" % len(stuff))
				allFound = True

				# TODO: Turn all cubes' lights off
				for x in stuff:
					x.set_lights(cozmo.lights.off_light)

				# Play "stackEm" !
				#stackEm()
				# Lookaround until Cozmo knows where all the cubes are:
				lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
				cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=60)
				print(cubes)
				lookaround.stop()

				if len(cubes) < 3:
					print("Error: Only found %d cubes" % len(cubes))
					quit()




				# Try and pickup the 1st cube
				current_action = robot.pickup_object(cubes[0], num_retries=3)
				current_action.wait_for_completed()
				if current_action.has_failed:
					code, reason = current_action.failure_reason
					result = current_action.result
					print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
					quit()

				# Now try to place that cube on the 2nd one
				current_action = robot.place_on_object(cubes[1], num_retries=3)
				current_action.wait_for_completed()
				if current_action.has_failed:
					code, reason = current_action.failure_reason
					result = current_action.result
					print("Place On Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
					quit()

				print("Cozmo successfully stacked 2 blocks!")

				# Exit
				quit()

		except concurrent.futures.TimeoutError:
			print("\nDidn't detect any taps for a while...\nExiting\n")
			quit()
    
cozmo.run_program(watch_cubes)

