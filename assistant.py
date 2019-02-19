import time
import pyttsx3
import webbrowser
import httplib, urllib, base64
import json
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import pyaudio
import wave
import pyglet
import playsound
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from pygame import mixer
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


app = Flask(__name__)
api = Api(app)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
EMAIL_OUTPUT_FILENAME = "email.wav"
MUSIC_PLAYER_OUTPUT_FILENAME = "music_player.wav"
MUSIC_STOPER_OUTPUT_FILENAME = "music_stoper.wav"
FRAMES = []
EMAIL_FRAMES = []
MUSIC_PLAYER_FRAMES = []
MUSIC_STOPER_FRAMES = []
P = pyaudio.PyAudio()
music_folder = 'D:\CodeCombat\mp3Songs'
music = ['\R','\W','\A']
MUSIC = False
EMAIL = False
sender_email_shubham = "bsss.3332@gmail.com"
sender_email_vivek = "agent47vivek@gmail.com"
receiver_email = "shubham.sharma@people10.com"
message = MIMEMultipart("alternative")
message["Subject"] = "Message from VoicePI"
message["From"] = sender_email_vivek
message["To"] = receiver_email
rows=3
columns=3
SPEAKER_DATA = [["Vivek","2314cf7d-5408-4608-b7b3-8cb48a9d5bf1",True],["Shubham","20102024-a5b6-4aa5-915c-4db2b0cf0307",True],["Ashika","2a226f34-0139-44eb-b08d-ac1430818ac3",False]]
mixer.init()
MUSIC_PLAYER = "Unknown"
MUSIC_STOPER = "Unknown"


# CORS(app)

@app.route("/")
def hello():
    speak('Hello Sir, I am your personal voice assistant Voice PI')
    greetMe()
    speak('How may I help you?')

    while True:
        global MUSIC
        global EMAIL
        global EMAIL_FRAMES
        global MUSIC_PLAYER
        global MUSIC_STOPER
        global sender_email_shubham
        global sender_email_vivek

        
        query = myCommand()
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'Shubham' in recipient:
                try:
                    speak("What is the body part ?")
                    message["Body"]=myCommand()
                    wf = wave.open(EMAIL_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(P.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(EMAIL_FRAMES))
                    wf.close()
                    EMAIL_FRAMES =[]
                    # print("IT REACHED HERE?")
                    recognize_speaker("email.wav","email")
                    # print(dir(audio))
                    # EMAIL_FRAMES.append(audio.frame_data)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    if EMAILER == "Vivek":
                        server.login(sender_email_vivek, 'enter your password')
                        server.sendmail(sender_email_vivek, receiver_email,message["Body"] )
                        server.close()
                        speak('Email sent!')
                    elif EMAILER == "Shubham":
                        server.login(sender_email_shubham, 'enter your password')
                        server.sendmail(sender_email_shubham, receiver_email,message["Body"] )
                        server.close()
                        speak('Email sent!')
                    elif EMAILER == "Ashika":
                        speak('Sorry Ashika you are not authorised to send an email')
                    elif EMAILER == "Unknown":
                        speak('Please enroll and authorise yourself to send an email')
                    EMAIL = False
                    EMAIL_FRAMES = []

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')
                    EMAIL = False
                    EMAIL_FRAMES = []

        
        elif 'stop music' in query or (MUSIC == True and 'music' in query):
            if MUSIC_PLAYER != MUSIC_STOPER:
                speak('Sorry '+ MUSIC_STOPER + ' you are not the one who started the music')
                continue; 
            mixer.music.stop()
            MUSIC = False
        
        elif 'nothing' in query or 'abort' in query in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            print("* done recording")
            P.terminate()
            sys.exit()
            
        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(P.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(FRAMES))
            wf.close()
            sys.exit()
                                    
        elif 'play' in query and 'music' in query:
            random_music = music_folder  + random.choice(music) + '.mp3'
            speak('Okay, here is your music! Enjoy!') 
            mixer.music.load(random_music)
            mixer.music.play()
            MUSIC = True
         
        else:
            query = query
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak(results)
        
            except:
                webbrowser.open('www.google.com')
        

        speak('Next Command! Sir!')

    return jsonify({'text':'Hello World!'})

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('THE87U-AXRX25RYLE')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)


def speak(audio):
    print('Computer: ' + audio)
    engine = pyttsx3.init();
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 16:
        speak('Good Afternoon!')

    if currentH >= 16 and currentH !=0:
        speak('Good Evening!')

def recognize_speaker(file,rqtype):
    global SPEAKER_DATA
    global rows
    global columns
    global MUSIC_PLAYER
    global MUSIC_STOPER
    global EMAILER
    global MUSIC_PLAYER_FRAMES
    global MUSIC_STOPER_FRAMES
    speaker_assigned = False
    print("Processing..")
    # print("its coming here",file)
    w = open(file, "rb")

    headers = {
        # Request headers
        'Content-Type': 'application/multipart/form-data',
        'Ocp-Apim-Subscription-Key': '12b3f53ce7e84ebab5a142acb006a3cd',
    }

    params = urllib.urlencode({
        # Request parameters
        'shortAudio': 'True',
    })

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/spid/v1.0/identify?identificationProfileIds=20102024-a5b6-4aa5-915c-4db2b0cf0307,2314cf7d-5408-4608-b7b3-8cb48a9d5bf1,2a226f34-0139-44eb-b08d-ac1430818ac3,1e60e469-f1de-43b0-8c91-cddc20c88224,fd50dad3-f01e-442f-a02c-ae7d7af38b4f&%s" % params, w, headers)
        response = conn.getresponse()
        data1 = response.getheader('Operation-Location')
        # print(response.getheader('Operation-Location'))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    opId = data1.split("operations/")[1]
    print(opId)

    time.sleep(5)
    headers = {
    # Request headers
        'Ocp-Apim-Subscription-Key': '12b3f53ce7e84ebab5a142acb006a3cd',
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/spid/v1.0/operations/"+opId+"?%s" % params, opId, headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data)
        # speakerId = jsondata['processingResult']['identifiedProfileId']
        # print(type(jsondata['processingResult']['identifiedProfileId']))
        # d = json.loads(j)
        # print d['glossary']['title']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    speakerId = jsondata['processingResult']['identifiedProfileId']
    confidence = jsondata['processingResult']['confidence']
    rows=3
    columns=3
    # from array import *
    SPEAKER_DATA = [["Vivek","2314cf7d-5408-4608-b7b3-8cb48a9d5bf1",True],["Shubham","20102024-a5b6-4aa5-915c-4db2b0cf0307",True],["Ashika","2a226f34-0139-44eb-b08d-ac1430818ac3",False]]

    for i in range(rows):
        for j in range(columns):
            if SPEAKER_DATA[i][j] == speakerId:
                speaker = SPEAKER_DATA[i][j-1]
                speaker_assigned = True
                print(speaker)

    if rqtype == "music":      
        if file == "music_player.wav":
            if speaker_assigned:
                MUSIC_PLAYER = speaker
            else :
                MUSIC_PLAYER = "Unknown"
        if file == "music_stoper.wav":
            if speaker_assigned:
                MUSIC_STOPER = speaker 
            else : 
                MUSIC_STOPER = "Unknown"
        
        print(MUSIC_PLAYER,"player")
        print(MUSIC_STOPER,"stoper")
        MUSIC_PLAYER_FRAMES = []
        MUSIC_STOPER_FRAMES = []
    elif rqtype == "email":
        print("EMAIL REQUEST")
        if speaker_assigned:
            EMAILER = speaker
            print(EMAILER)
        else:
            EMAILER = 'Unknown'
            print(EMAILER)
        EMAIL_FRAMES = []
    



    



def myCommand():
    global EMAIL
    global EMAILER
    global MUSIC
    global MUSIC_PLAYER
    global MUSIC_STOPER
    global SPEAKER_DATA
    r = sr.Recognizer()   
    # print(dir(sr.Microphone.__dict__))                                                                                
    with sr.Microphone(sample_rate = 16000) as source:                                                                       
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        # print("CAME HERE?")
        # print(dir(audio.sample_rate))
        FRAMES.append(audio.frame_data)
        # print(EMAIL)
        if EMAIL == True:
            EMAIL_FRAMES.append(audio.frame_data)

    try:
        query = r.recognize_google(audio, language='en-in')
        if "email" in query:
            EMAIL_FRAMES.append(audio.frame_data)
            EMAIL = True
        if 'play' in query and 'music' in query :
            MUSIC_PLAYER_FRAMES.append(audio.frame_data)
            wf = wave.open(MUSIC_PLAYER_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(P.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(MUSIC_PLAYER_FRAMES))
            wf.close()
            recognize_speaker("music_player.wav","music")
            print("Music player = " , MUSIC_PLAYER)
        if 'stop' in query and 'music' in query :
            MUSIC_STOPER_FRAMES.append(audio.frame_data)
            wf = wave.open(MUSIC_STOPER_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(P.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(MUSIC_STOPER_FRAMES))
            wf.close()
            recognize_speaker("music_stoper.wav","music")
            print("Music stopper = " , MUSIC_STOPER)
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query

     

if __name__ == '__main__':
     app.run(port=5002)