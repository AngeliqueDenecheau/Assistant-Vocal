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
import random

from gtts import gTTS
from io import BytesIO
import pygame
from pydub import AudioSegment

from api_calls import *

from deep_translator import GoogleTranslator

from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.wsd import lesk
from nltk import pos_tag, word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.chunk.regexp import *
import os

### A point enviser
jar = "/home/etud/Documents/projet/Assistant-Vocal/stanford-postagger-4.2.0.jar"
model = "/home/etud/Documents/projet/Assistant-Vocal/french-ud.tagger"
java_path = "/usr/bin/java"

os.environ['JAVAHOME'] = java_path
####

listener = sr.Recognizer()
wikipedia.set_lang("fr")
default_navigator = 'firefox'

def langageProcessing(sentence):
    '''
    Process a query by tokenizing it, tagging it, and applying a grammar on it, then remove useless words to keep keywords.

    The sentence is tagged as subsentences (Noun group, verbal group ..) with each word labelized (Noun, adjective, verb ...)
    which allow us to remove unimportant words (determiners for a google search for instance)

    :param sentence: The sentence to process
    :return: Keywords
    '''

    pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
    res = pos_tagger.tag(sentence.split())

    grammar = "NP: {<DET>?<ADJ>?<NOUN><ADJ>?|<DET>?<ADJ>?<PROPN><ADJ?>|<ADJ>|<NOUN>|<PROPN>|<ADP>|<DET>|<NUM>} \n PP: {<NP>*} \n VP : {<PRON>?<VERB><PRON>?|<PRON>?<AUX><PRON>?}"
    parser = RegexpParser(grammar)
    parsed = parser.parse(res)

    # Keep NOUN / VERB / PROPN / ADJ / NUM /
    cut = ""
    tags = ("NOUN", "PROPN", "ADJ", "NUM", "VERB")

    cut = removeTag(parsed, tags)

    return cut

def removeTag(sentence, tags):
    '''
    Removes tags from pos_tagged sentence to get a clean list of words choosen with the "tags" param

    :param sentence: The sentence to clean
    :param tags: The tags to keep
    :return: A list of words
    '''

    action = ""
    complement = ""

    if len(sentence) > 1:
        if isinstance(sentence, tuple):
            if sentence[1] in tags:
                if sentence[1] == "VERB":
                    action += sentence[0] + " "
                else:
                    complement += sentence[0] + " "
        else:
            for i in range(len(sentence)):
                cutAction, cutComplement = removeTag(sentence[i], tags)
                action += cutAction
                complement += cutComplement
    else:
        cutAction, cutComplement = removeTag(sentence[0], tags)
        action += cutAction
        complement += cutComplement

    return (action, complement)

def getSynonyms(word):
    '''
    Get synonyms of a word

    :param word: The word to get a synonym of
    :return: The synonyms
    '''
    lang = 'fra'

    sent = TreebankWordTokenizer().tokenize(word)
    synsets = [lesk(sent, w, 'n') for w in sent]

    for ws in sent:
        return [n for synset in wn.synsets(ws, lang=lang) for n in synset.lemma_names(lang)]

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
    Wait for the user to talk

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
        print("err")
        pass


def run_jacqueline():
    '''
    Main function of Jacqueline, use keywords to perform an action

    :return: Nothing
    '''

    command = take_command()

    action, complement = langageProcessing(command)

    print(action, complement)

    if command == None:
        return

    if action != "":
        print("test")
        doAction(action, complement)
    else:
        print("hmm")
        getInformation(complement)


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


def doAction(action, command):
    '''
    Jacqueline does an action

    :param action: The action Jacqueline has to do
    :param command: The command Jacqueline has to do
    '''
    # Plays a video on youtube
    if 'joue' in action:
        print('commande jouer')
        # song = command.replace('joue ', '')
        song = command
        talk(song + ' en cours de lecture')
        pywhatkit.playonyt(song)

    # Launch an app
    elif 'ouvre' in action or 'lance' in action:
        print('commande ouvre/lance')
        # software = command.replace('ouvre ', '')
        # software = command.replace('lance ', '')
        try:
            subprocess.Popen('/usr/bin/' + command)
            talk('Ouverture de ' + command)
        except FileNotFoundError:
            talk(command + ' n\'est pas installé sur cet ordinateur')

    # Make a Google search
    elif 'recherche' in action:
        print('commande recherche')
        command = command.replace('recherche ', '')

        navigator = default_navigator
        if command != "":
            navigator = get_navigator(command)
            # command = command.replace('dans ', '')
            if navigator != None:
                command = command.replace(navigator, '')
            else:
                return

        internet_research(command, navigator)

    # Tells a quote
    elif 'citation' in command or 'cite' in action:  # Not entirely taken care of
        command = command.replace('citation ', '')
        # action = action.replace('cite ', '')
        if 'animé' in command:
            command = command.replace('animé ', '')
            print('commande citation')
            talk(anime_quote())

    # Shutdown Jacqueline
    elif 'dormir' in action:  # Stop Jacqueline
        talk("Bonne nuit")
        exit()

    # Doesn't understand
    else:
        getInformation(command)

def getInformation(command):
    '''
    Jaqueline get information
    
    :param command: The command Jacqueline has to do
    '''

    # Gives fiscal information
    if 'fiscal' in command or 'entité' in command:
        talk(documentation_fiscal_entities_france())
        print("L'api va donner un cours de SES")

    # Tells the time
    elif 'heure' in command:
        print('commande heure')
        time = datetime.datetime.now().strftime('%H:%M')
        talk('il est actuellement ' + time)

    # Gives French holiday
    elif 'ferié ' in command:
        talk(jours_feries())
        print('commande jour ferié')

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

    # Tells a fact
    elif 'fact' in command:
        complement = command.replace('fact ', '')
        print('commande fact')
        if 'axolot' in complement:
            talk(axolot_fact())
        elif 'animé' in complement:  # Not entirely taken care of
            talk(anime_fact())
        elif 'chuck' in complement:  # donne un fact
            print('commande chuck norris fact')
            talk(chuck_fact())
        else:
            print("random fact")
            talk(random.choice([axolot_fact(), chuck_fact()]))

    # Doesn't understand
    else:
        print('commande introuvable')
        talk('je n\'ai pas compris')

# Jacqueline loop
while True:
    run_jacqueline()
