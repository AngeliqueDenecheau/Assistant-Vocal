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

def jours_feries():
    '''
        Make an API call to get all the special holliday day in France for 2021

        :return: A list of the special holliday day in France
    '''
    response = rq.get("https://calendrier.api.gouv.fr/jours-feries/metropole/2021.json")
    jours_feries = "";
    for a in response.json():
        jours_feries = jours_feries + " et le " + a + " " + response.json()[a];
    return "Les prochains jours fériés sont " + jours_feries


def documentation_fiscal_entities_france():
    '''
        Make an API call to get information about different fiscal entities in france

        :return: A Chuck Norris fact in English
    '''
    response = rq.get("https://fr.openfisca.org/api/latest/entities")
    collect_documentation = "";
    for a in response.json():
        collect_documentation = collect_documentation + " " + response.json()[a]["documentation"];
    return "Voilà des informations sur les différentes entités fiscales en France " + collect_documentation
