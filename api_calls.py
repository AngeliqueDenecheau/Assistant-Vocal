#conda install Requests
import requests as rq

def anime_quote():
    '''
    Make an API call to get an anime quote

    :return: An anime quote in English
    '''

    response = rq.get("https://animechan.vercel.app/api/random")
    return response.json()["character"]+" says: "+response.json()["quote"]

def anime_fact(anime):
    '''
    Make an API call to get an anime fact

    :param anime: The anime from which we want a fact
    :return: An anime fact in English
    '''

    response = rq.get("https://anime-facts-rest-api.herokuapp.com/api/v1/")
    return "Anime fact: " + response.json()

def axolot_fact():
    '''
        Make an API call to get an axolotl fact

        :return: An axolotl fact in English
    '''

    response = rq.get("https://axoltlapi.herokuapp.com/")
    return "Axolot fact: " + response.json()["facts"]

def chuck_fact():
    '''
        Make an API call to get a Chuck Norris fact

        :return: A Chuck Norris fact in English
    '''
    response = rq.get("https://api.chucknorris.io/jokes/random")
    return "Chuck norris fact: " + response.json()["value"]