import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai.api_key=''

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init() 
engine.setProperty('rate', 170) 
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
name = "Zavi"
greetings = [f"Hello, this is {name}. How may I assist you today?"]

# Function to handle the text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen for the wake word "yes"
def listen_for_wake_word(source):
    print("Listening for 'Hello'...")
    while True:
        try:
            audio = r.listen(source, timeout=1, phrase_time_limit=2)
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                speak(np.random.choice(greetings))
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            continue
        except sr.WaitTimeoutError:
            continue

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening for command...")
    while True:
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print(".....Recognizing wait....")
            speak("Recognizing wait")
            print(f"You said: {text}")
            if not text:
                continue

            if "stop" in text.lower():
                print("Stopping assistant.")
                speak("Goodbye")
                break

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}],
                request_timeout=10  # Set a timeout for the OpenAI API response
            )
            response_text =response["choices"][0]["message"]["content"]
            print(response_text)

            # Speak the response
            speak(response_text)

        except sr.UnknownValueError:
            print("Didn't catch that, please repeat.")
            speak("I didn't catch that, please repeat.")
        
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak(f"Could not request results; {e}")

        except sr.WaitTimeoutError:
            print("Listening timeout. Please speak again.")
            continue

        except openai.error.Timeout:
            print("OpenAI API request timed out.")
            speak("Sorry, the response took too long. Please try again.")
        
        print("Listening for next command or 'stop' to end...")

# Use the default microphone as the audio source
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
    listen_for_wake_word(source)
