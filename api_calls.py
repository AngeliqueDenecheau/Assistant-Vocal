#conda install Requests
import requests as rq
from deep_translator import GoogleTranslator

langueSource = "en"
langueDest = "fr"

def anime_quote():
    response = rq.get("https://animechan.vercel.app/api/random")
    return GoogleTranslator(source=langueSource, target=langueDest).translate(response.json()["character"]+" says: "+response.json()["quote"])

def anime_fact(anime):
    response = rq.get("https://anime-facts-rest-api.herokuapp.com/api/v1/")
    return "Anime fact: " + GoogleTranslator(source=langueSource, target=langueDest).translate(response.json())

def axolot_fact():
    response = rq.get("https://axoltlapi.herokuapp.com/")
    return "Axolot fact: " + GoogleTranslator(source=langueSource, target=langueDest).translate(response.json()["facts"])

def chuck_fact():
    response = rq.get("https://api.chucknorris.io/jokes/random")
    return "Chuck norris fact: " + GoogleTranslator(source=langueSource, target=langueDest).translate(response.json()["value"])