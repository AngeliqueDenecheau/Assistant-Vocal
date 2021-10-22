# Problème pyAudio : sudo apt install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
# Problème libespeak : sudo apt-get install espeak

import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys
import subprocess

from gtts import gTTS
from io import BytesIO
import pygame
from pydub import AudioSegment

from api_calls import *

from deep_translator import GoogleTranslator

listener = sr.Recognizer()
wikipedia.set_lang("fr")
default_navigator = 'firefox'


def talk(text, langueDest = "fr"):
    '''
    Make Jacqueline talk (in French)

    :param text: The text to say
    :param langueDest: The langage Jacqueline talks in
    '''

    # Sources might be other than English, so we let google translate decide
    text = GoogleTranslator(source="auto", target=langueDest).translate(text)

    mp3_fp = BytesIO()
    wav_fp = BytesIO()
    tts = gTTS(text, lang=langueDest, slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    sound = AudioSegment.from_file(mp3_fp)
    wav_fp = sound.export(mp3_fp, format="wav")
    pygame.mixer.init()
    pygame.mixer.music.load(wav_fp)
    pygame.mixer.music.play()


def take_command():
    '''
    Wait for the user to talk and tokenize his sentence

    :return: The user's command
    '''

    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, None, "fr-FR")
            command = command.lower()
            print(command)
            if 'jacqueline' in command:
                command = command.replace('jacqueline ', '')
                print(command)
                return command
    except:
        pass


def run_jacqueline():
    '''
    Main function of Jacqueline, use keywords to perform an action

    :return: Nothing
    '''

    # No command
    command = take_command()
    if command == None:
        return

    # Plays a video on youtube
    if 'joue ' in command:
        print('commande jouer')
        song = command.replace('joue ', '')
        talk(song + ' en cours de lecture')
        pywhatkit.playonyt(song)

    # Tells the time
    elif 'heure' in command:
        print('commande heure')
        time = datetime.datetime.now().strftime('%H:%M')
        talk('il est actuellement ' + time)

    # Looks up somebody on wikipedia
    elif 'qui est' in command:
        print('commande qui est')
        person = command.replace('qui est ', '')
        info = wikipedia.summary(person, 1)
        talk(info)

    # Tells a joke
    elif 'blague' in command:
        print('commande blague')
        talk(pyjokes.get_joke())

    # Launch an app
    elif 'ouvre' in command or 'lance' in command:
        print('commande ouvre/lance')
        software = command.replace('ouvre ', '')
        software = command.replace('lance ', '')
        try:
            subprocess.Popen('/usr/bin/' + software)
            talk('Ouverture de ' + software)
        except FileNotFoundError:
            talk(software + ' n\'est pas installé sur cet ordinateur')

    # Make a Google search
    elif 'recherche' in command:
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

    # Shutdown Jacqueline
    elif 'dormir' in command:  # Stop Jacqueline
        talk("Bonne nuit")
        exit()

    # Tells a fact
    elif 'fact' in command:
        print('commande fact')
        if 'axolot' in command:
            talk(axolot_fact())
        elif 'animé' in command:
            talk(anime_fact(""))
        elif 'chuck' in command:  # donne un fact
            print('commande chuck norris fact')
            talk(chuck_fact())

    # Tells a quote
    elif 'citation' in command or 'cite' in command:
        if 'animé' in command:
            print('commande citation')
            talk(anime_quote())

    # Doesn't understand
    else:
        print('commande introuvable')
        talk('je n\'ai pas compris')


def get_navigator(command):
    '''
    Function used to get the specified navigator to search in

    :param command: The user's command
    :return: The navigator specified by the user
    '''

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
    '''
    Make a reasearch on the internet

    :param text: What to search
    :param navigator: The navigator to use
    '''

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

# Jacqueline loop
while True:
    run_jacqueline()
