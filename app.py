import os
import google.generativeai as genai
from apikey import api_data  # Your Gemini API Key
import speech_recognition as sr
import pyttsx3
import webbrowser

# Configure Gemini
genai.configure(api_key=api_data)
model = genai.GenerativeModel("models/gemini-1.5-flash")  # Fast, lightweight, compatible

# Voice output setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def Reply(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        print("Error generating reply:", e)
        return "Sorry, I couldn't process that."

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening .......')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing ....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query} \n")
    except Exception as e:
        print("Say that again .....")
        return "none"
    return query.lower()

# Initial greeting
speak("Hello, how are you?")

if __name__ == '__main__':
    while True:
        query = takeCommand()
        if query == "none":
            continue

        if "open youtube" in query:
            webbrowser.open('https://www.youtube.com')
            continue
        if "open google" in query:
            webbrowser.open('https://www.google.com')
            continue
        if "bye" in query or "exit" in query:
            speak("Goodbye!")
            break

        # Gemini Response
        ans = Reply(query)
        print("Gemini:", ans)
        speak(ans)
