import time
import speech_recognition as sr
import sys
import json
import pprint

if __name__ == '__main__':
    with open('phrases2.json') as f:
        phrases = dict(json.load(f))

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        for phrase in phrases:
            for i in range(2):

                print("Please say: ", phrase)
                print("Listening ...")
                audio = r.listen(source)

                try:
                    print("Processing ...")
                    text = r.recognize_google(audio)
                    phrases[phrase]['paraphrases'].append(text)
                except:
                    print("Api Error")
                    time.sleep(2)

    with open("phrases2.json", "w") as write_file:
        json.dump(phrases, write_file, indent=4)