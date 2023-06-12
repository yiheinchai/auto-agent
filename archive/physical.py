import speech_recognition as sr
import pyttsx3
import cv2
import numpy as np
import time
from transformers import pipeline

# Adds ability to move, see and listen to speech
class PhysicalAutonomousLLM:
    def __init__(self):
        self.text_to_speech = pyttsx3.init()
        self.text_to_speech.setProperty('rate', 150)
        self.text_to_speech.setProperty('volume', 1.0)
        self.speech_recognizer = sr.Recognizer()
        self.camera = cv2.VideoCapture(0)
        self.chatbot = pipeline('text2text-generation', model='GPT2')
        self.action = None

    def execute_action(self):
        if self.action == 'say':
            self.text_to_speech.say(self.output)
            self.text_to_speech.runAndWait()
        elif self.action == 'add_method':
            method_name = self.output.split(" ")[-1]
            method_code = self.output.split("add method ")[-1].split(" to class")[0]
            setattr(self, method_name, method_code)
            print(f"Method {method_name} added to object.")
        elif self.action == 'modify_method':
            method_name = self.output.split(" ")[-1]
            method_code = self.output.split("modify method ")[-1].split(" to class")[0]
            setattr(self, method_name, method_code)
            print(f"Method {method_name} modified in object.")
        elif self.action == 'execute_code':
            code = self.output.split("execute code ")[-1]
            exec(code)
            print("Code executed.")
        elif self.action == 'move_forward':
            # code to move forward
            print("Moving forward.")
        elif self.action == 'turn_left':
            # code to turn left
            print("Turning left.")
        elif self.action == 'turn_right':
            # code to turn right
            print("Turning right.")
        else:
            print("Invalid action.")

    def process_input(self):
        with sr.Microphone() as source:
            self.speech_recognizer.adjust_for_ambient_noise(source)
            audio = self.speech_recognizer.listen(source)
            try:
                self.input_text = self.speech_recognizer.recognize_google(audio)
                print(f"Input: {self.input_text}")
            except sr.UnknownValueError:
                self.input_text = None
                print("Could not recognize input.")
    
    def process_output(self):
        if self.input_text is not None:
            response = self.chatbot(self.input_text)[0]['generated_text']
            self.action = response.split(':')[0]
            self.output = response.split(':')[1].strip()
            print(f"Output: {self.output}")
        else:
            self.action = None
            self.output = None

    def run(self):
        while True:
            self.process_input()
            self.process_output()
            self.execute_action()

            # code to process sensor data and update self.state

            time.sleep(0.1)

if __name__ == '__main__':
    llm = AutonomousLLM()
    llm.run()
