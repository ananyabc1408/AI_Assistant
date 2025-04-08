import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import pyjokes
import random
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty(name='rate', value=150)  # Adjust speech speed

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet based on time of day"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 17:
        greet = "Good afternoon"
    elif 17 <= hour < 21:
        greet = "Good evening"
    else:
        greet = "Hello"
    speak(f"{greet}, Ananya B C! How can I assist you?")

def listen():
    """Listen for voice commands"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Could not connect to Google Speech Recognition.")
        return ""

def play_local_music(folder_path):
    """Play a random music file from a folder"""
    try:
        songs = os.listdir(folder_path)
        music_files = [song for song in songs if song.endswith(('.mp3', '.wav'))]
        if music_files:
            song = random.choice(music_files)
            os.startfile(os.path.join(folder_path, song))
            speak(f"Playing {song}")
        else:
            speak("No music files found in the folder.")
    except Exception as e:
        speak("I couldn't play music from your folder.")
        print(e)

def execute_command(command):
    """Execute command based on voice input"""
    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query}")
        pywhatkit.search(query)

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=1)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
        except Exception:
            speak("Sorry, I couldn't find that on Wikipedia.")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "play music" in command:
        music_folder = "C:/Users/YourUsername/Music"  # <- Replace with your music folder path
        play_local_music(music_folder)

    elif "how are you" in command:
        speak("I'm doing great, thanks for asking! How can I help you today?")

    elif "tell me something cool" in command:
        speak("Did you know? Octopuses have three hearts and blue blood!")

    elif "exit" in command or "goodbye" in command:
        speak("Goodbye! Have a nice day.")
        exit()

    else:
        speak("I didn't understand that command.")

# Run the assistant
greet_user()
while True:
    command = listen()
    if command:
        execute_command(command)
