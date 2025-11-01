from click import command
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import webbrowser
import os
import smtplib

#Intialize Voice Assistant
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! Jennie in your service. How can I help you?")

    elif hour>=12 and hour<18:
        speak("Good Afternoon! Jennie in your service. How can I help you?")   

    else:
        speak("Good Evening! Jennie in your service. How can I help you?")         

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open helper' in query:
            webbrowser.open("blackbox.ai")

        elif 'open amazon' in query:
            webbrowser.open("amazon.com")

        elif 'open flipkart' in query:
            webbrowser.open("flipkart.com")

        elif 'open compiler' in query:
            webbrowser.open("programiz.com")

        elif 'open spotify' in query:
            webbrowser.open("spotify.com")