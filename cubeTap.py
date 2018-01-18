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

async def watch_cubes(robot: cozmo.robot.Robot):
    print("Cozmo is waiting for cubes to be tapped")

    while(True):
        try:
            cube = await robot.world.wait_for(cozmo.objects.EvtObjectTapped)
            print("\nCube %d tapped %d time(s), intensity: %d, duration: %d, Visible: %s" % (cube.obj.object_id, cube.tap_count, cube.tap_intensity, cube.tap_duration, cube.obj.is_visible))
            #print(cube)
        #except concurrent.futures._base.TimeoutError:
        except:
            print("\nDidn't detect any taps for a while...\nExiting\n")
            quit()
    
cozmo.run_program(watch_cubes)

'''
For example, if you only need to know whether a particular cube has been
tapped, you can call the :meth:`~cozmo.event.Dispatcher.wait_for` method
directly on that cube's :class:`cozmo.objects.LightCube` instance.  Eg::
    my_cube.wait_for(cozmo.objects.EvtObjectTapped)
If, however, you want to wait for any cube to be tapped, you could instead
call the :meth:`~cozmo.event.Dispatcher.wait_for` method on the
:class:`World` object instead.  Eg::
    robot.world.wait_for(cozmo.objects.EvtObjectTapped)
In either case, ``wait_for`` will return the instance of the event's
:class:`~cozmo.objects.EvtObjectTapped` class, which includes a
:attr:`~cozmo.objects.EvtObjectTapped.obj` attribute, which identifies
exactly which cube has been tapped.
'''
