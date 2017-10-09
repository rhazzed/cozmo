#!/usr/bin/env python3

import pyaudio
import speech_recognition as sr
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

p = pyaudio.PyAudio()
micIdx=0
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info['index'], info['name'])
    if (info['name'].startswith('C-Media')):
        print("    *** Found C-Media device! ***")
        micIdx = i
    if (info['name'].startswith('USB')):
        print("    *** Found USB device! ***")
        micIdx = i
print("\n")

r = sr.Recognizer()
while True:
    with sr.Microphone(device_index=micIdx) as source:
        answr = input("Press <Enter> when you want to start listening (or 'q' to Quit): ")
        if answr == "q":
            break
        print("\nListening...")
        audio = r.listen(source)
        print("Finished listening. Starting recognition...")

    try:
        #print("         " + r.recognize_google(audio))
        #print("         " + r.recognize_wit(audio))	# Did not try - didn't get API key either...
        #
        # THE FOLLOWING WORKS (Sphinx)! - 
        #print("    " + r.recognize_sphinx(audio))	# WORKS!
        print("Trying sphinx...")
        sphinx_out = r.recognize_sphinx(audio)
        #
        print("Trying Google...")
        google_out = r.recognize_google_cloud(audio)

        print("    Sphinx: " + sphinx_out)
        print("    Google: " + google_out)
    except:
        print("\t<<Could not understand audio>>")
    print("")

print("\nExiting\n")
