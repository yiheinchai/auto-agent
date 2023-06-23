def create_appointment_database():
    import sqlite3

    # Connect to or create the database file
    conn = sqlite3.connect("appointments.db")

    # Create a cursor object to execute SQL commands
    c = conn.cursor()

    # Create a table to store appointment information
    c.execute(
        """CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 date TEXT NOT NULL,
                 time TEXT NOT NULL,
                 description TEXT NOT NULL);"""
    )

    # Save changes and close the connection
    conn.commit()
    conn.close()


class Appointment:
    def __init__(self, date, time, person):
        self.date = date
        self.time = time
        self.person = person


class Schedule:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def display_schedule(self):
        for i, appointment in enumerate(self.appointments):
            print(
                f"{i+1}. {appointment.person} on {appointment.date} at {appointment.time}"
            )


schedule = Schedule()

# example usage
appointment1 = Appointment("2022-01-01", "10:00am", "John")
schedule.add_appointment(appointment1)

appointment2 = Appointment("2022-01-02", "2:30pm", "Jane")
schedule.add_appointment(appointment2)

schedule.display_schedule()


def identify_platforms():
    platforms = [
        "Alexa",
        "Google Home",
        "Apple HomeKit",
        "Microsoft Cortana",
        "Samsung SmartThings",
    ]
    print("Platform(s) to integrate with:")
    for platform in platforms:
        print("- " + platform)


def add_method(self, function):
    setattr(self, function.__name__, function)


def add_method(self, func):
    setattr(self, func.__name__, func)


import speech_recognition as sr
import pyautogui

# create instance of the Recognizer class
r = sr.Recognizer()


# define a function to execute actions based on voice commands
def execute_command(command):
    if "up" in command:
        pyautogui.press("up")
    elif "down" in command:
        pyautogui.press("down")
    elif "left" in command:
        pyautogui.press("left")
    elif "right" in command:
        pyautogui.press("right")
    elif "scroll up" in command:
        pyautogui.scroll(1)
    elif "scroll down" in command:
        pyautogui.scroll(-1)
    else:
        print("Command not recognized")


# define a function to listen to microphone and recognize voice commands
def listen_microphone():
    # use microphone as source of audio input
    with sr.Microphone() as source:
        print("Listening...")
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # record audio from microphone
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        command = r.recognize_google(audio)
        print("You said: " + command)
        # execute corresponding action based on voice command
        execute_command(command.lower())
    except sr.UnknownValueError:
        # speech was unintelligible
        print("Could not understand audio")
    except sr.RequestError as e:
        # Google Speech Recognition service error
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


# continuously listen for voice commands until program is interrupted
while True:
    listen_microphone()
    break


def alexa_skill(request):
    if request["request"]["type"] == "LaunchRequest":
        # Handle the Alexa skill launch event
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Welcome to my Alexa skill!",
                }
            },
        }
    elif request["request"]["type"] == "IntentRequest":
        intent = request["request"]["intent"]["name"]
        if intent == "hello":
            # Handle the hello intent
            response = {
                "version": "1.0",
                "response": {
                    "outputSpeech": {"type": "PlainText", "text": "Hello there!"}
                },
            }
        else:
            # Handle unknown intents
            response = {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "I'm sorry, I don't understand.",
                    }
                },
            }
    else:
        # Handle unknown request types
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I'm sorry, I don't understand.",
                }
            },
        }

    return response

import time

def set_reminder():
    reminder_time = input("Enter reminder time in format HH:MM:SS\n")
    reminder_note = input("Enter reminder note\n")
    current_time = time.strftime("%H:%M:%S")
    
    while current_time != reminder_time:
        current_time = time.strftime("%H:%M:%S")
        time.sleep(1)
        
    print(reminder_note)
    
import notify2

def send_notification(title, message):
    notify2.init("Notification System")
    n = notify2.Notification(title, message)
    n.set_timeout(5000)
    n.show()

import datetime

reminders = []

def add_reminder():
    description = input("Enter a description for the reminder: ")
    year = int(input("Enter the year for the reminder (e.g. 2022): "))
    month = int(input("Enter the month for the reminder (1-12): "))
    day = int(input("Enter the day for the reminder (1-31): "))
    hour = int(input("Enter the hour for the reminder (0-23): "))
    minute = int(input("Enter the minute for the reminder (0-59): "))
    date = datetime.datetime(year, month, day, hour, minute)
    reminders.append((date, description))
    print("Reminder added successfully.")

def delete_reminder():
    index = int(input("Enter the index of the reminder to delete: "))
    if index >= len(reminders):
        print("Invalid index.")
    else:
        del reminders[index]
        print("Reminder deleted successfully.")

def print_reminders():
    if not reminders:
        print("No reminders.")
        return
    print("Current reminders:")
    for i, reminder in enumerate(reminders):
        date, description = reminder
        print(f"{i}: {description} at {date}")

def main():
    print("Welcome to the reminder app.")
    while True:
        print("-" * 20)
        print("Options:")
        print("1. Add a reminder")
        print("2. Delete a reminder")
        print("3. Print all reminders")
        print("4. Quit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_reminder()
        elif choice == 2:
            delete_reminder()
        elif choice == 3:
            print_reminders()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
