#!/usr/bin/env python3

import pyaudio
import speech_recognition as sr

p = pyaudio.PyAudio()
micIdx=0
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info['index'], info['name'])
    if (info['name'].startswith('C-Media')):
        print("    *** Found C-Media device! ***")
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
        #print("         " + r.recognize_wit(audio))
        print("    " + r.recognize_sphinx(audio))
    except LookupError:
        print("Could not understand audio")
    print("")

print("\nExiting\n")
