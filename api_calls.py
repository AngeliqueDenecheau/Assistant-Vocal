#conda install Requests
import requests as rq

def anime_quote():
    response = rq.get("https://animechan.vercel.app/api/random")
    return response.json()["quote"]

def anime_fact(anime):
    response = rq.get("https://anime-facts-rest-api.herokuapp.com/api/v1/")
    return "Anime fact: " + response.json()

def axolot_fact():
    response = rq.get("https://axoltlapi.herokuapp.com/")
    return "Axolot fact: " + response.json()["facts"]