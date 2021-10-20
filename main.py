# Problème pyAudio : sudo apt install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
# Problème libespeak : sudo apt-get install espeak

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys
import subprocess

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#engine.setProperty('voice', "french")
engine.runAndWait()

default_navigator = 'firefox'


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, None, "fr-FR")
            #command = listener.recognize_sphinx(voice, "fr-FR")
            command = command.lower()
            print(command)
            if 'jacqueline' in command:
                command = command.replace('jacqueline ', '')
                print(command)
                return command
    except:
        pass


def run_alexa():
    command = take_command()
    if command == None:
        return

    if 'joue' in command:
        print('commande jouer')
        song = command.replace('joue ', '')
        talk(song + ' en cours de lecture')
        pywhatkit.playonyt(song)
    elif 'heure' in command:
        print('commande heure')
        time = datetime.datetime.now().strftime('%H:%M')
        talk('il est actuellement ' + time)
    elif 'qui est' in command:
        print('commande qui est')
        person = command.replace('qui est ', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'blague' in command:
        print('commande blague')
        talk(pyjokes.get_joke())
    elif 'ouvre' in command or 'lance' in command:  # Ouvrir un logiciel
        print('commande ouvre/lance')
        software = command.replace('ouvre ', '')
        software = command.replace('lance ', '')
        try:
            subprocess.Popen('/usr/bin/' + software)
            talk('Ouverture de ' + software)
        except FileNotFoundError:
            talk(software + ' n\'est pas installé sur cet ordinateur')
    elif 'recherche' in command:  # Faire une recherche dans un navigateur
        print('commande recherche')
        command = command.replace('recherche ', '')

        navigator = default_navigator
        if 'dans' in command:
            navigator = get_navigator(command)
            command = command.replace('dans ', '')
            if navigator != None:
                command = command.replace(navigator, '')
            else:
                return

        internet_research(command, navigator)
    else:
        print('commande introuvable')
        talk('je n\'ai pas compris')


def get_navigator(command):
    if 'firefox' in command:
        return 'firefox'
    elif 'chrome' in command:
        return 'chrome'
    elif 'chromium' in command:
        return 'chromium'
    else:
        talk("je ne connais pas ce navigateur")
        return None


def internet_research(text, navigator):
    url = 'https://google.com/search?q=' + text
    try:
        webbrowser.get(navigator).open(url)
        talk('recherche de ' + text + ' dans ' + navigator)
    except webbrowser.Error:
        talk(navigator + ' n\'est pas installé sur cet ordinateur')

    """
    os = sys.platform
    if os == 'linux':
        webbrowser.get('/usr/bin/' + navigator + ' %s').open(url)
    elif os == 'darwin':
        webbrowser.get('open -a /Applications/Google\ Chrome.app %s').open(url)
    elif os == 'win32':
        webbrowser.get(
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(url)
    else:
        talk('Votre système d\'exploitation n\'est pas reconnu')
    """


while True:
    run_alexa()
