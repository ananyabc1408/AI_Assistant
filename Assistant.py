import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import pyjokes
import random

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for different voice

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I help you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting.")
            return ""

def open_website(command):
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com",
        "whatsapp": "https://whatsapp.com"
    }
    for key in sites:
        if key in command:
            speak(f"Opening {key}")
            webbrowser.open(sites[key])
            return True
    return False

def respond_fun_phrases(command):
    fun_responses = {
        "how are you": ["I'm great, thank you!", "Doing awesome, how about you?", "Feeling digital!"],
        "who are you": ["I'm your personal AI assistant!", "Just a friendly voice in your computer."],
        "tell me something funny": [pyjokes.get_joke()]
    }

    for phrase in fun_responses:
        if phrase in command:
            speak(random.choice(fun_responses[phrase]))
            return True
    return False

def run_assistant():
    greet_user()
    while True:
        command = take_command()

        if not command:
            continue

        if "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            speak("Searching Wikipedia...")
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Can you be more specific?")
            except Exception as e:
                speak("Couldn't find anything on Wikipedia.")

        elif "play music" in command or "play song" in command:
            speak("What song would you like to hear?")
            song_command = take_command()
            if song_command:
                speak(f"Playing {song_command} on YouTube")
                pywhatkit.playonyt(song_command)

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif open_website(command):
            continue

        elif respond_fun_phrases(command):
            continue

        elif "stop" in command or "exit" in command or "goodbye" in command:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("I'm not sure how to help with that yet, but I'm learning!")

if _name_ == "_main_":
    run_assistant()
