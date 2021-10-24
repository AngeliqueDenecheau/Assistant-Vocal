#conda install Requests
import requests as rq

# -- QUOTES

def anime_quote(command=""):
    """
    Make an API call to get an anime quote

    :param command: The remainder of the command
    :return: An anime quote in English
    """

    response = rq.get("https://animechan.vercel.app/api/random")
    return response.json()["character"]+" says: "+response.json()["quote"]

# -- FACTS

def anime_fact(command=""):
    """
    Make an API call to get an anime fact

    :param command: The remainder of the command
    :return: An anime fact in English
    """

    response = rq.get("https://anime-facts-rest-api.herokuapp.com/api/v1/")
    return "Anime fact: " + response.json()

def axolot_fact():
    """
    Make an API call to get an axolotl fact

    :return: An axolotl fact in English
    """
    response = rq.get("https://axoltlapi.herokuapp.com/")

    if (response.status_code == 200):
        return "Axolot fact: " + response.json()["facts"]
    else:
        return "Je n'ai pas de fact sur les axolotls aujourd'hui, je m'excuse pour le désagrément"

def chuck_fact():
    """
    Make an API call to get a Chuck Norris fact

    :return: A Chuck Norris fact in English
    """
    response = rq.get("https://api.chucknorris.io/jokes/random")
    return "Chuck norris fact: " + response.json()["value"]


# -- Miscellaneous legislative

def jours_feries(command=""):
    """
    Make an API call to get all the special holiday day in France for 2021

    :param command: The remainder of the command
    :return: A list of the special holiday day in France
    """
    response = rq.get("https://calendrier.api.gouv.fr/jours-feries/metropole/2021.json")
    jours_feries = "";
    for a in response.json():
        jours_feries = jours_feries + " et le " + a + " " + response.json()[a];
    return "Les prochains jours fériés sont " + jours_feries


def documentation_fiscal_entities_france(command=""):
    """
    Make an API call to get information about different fiscal entities in france

    :param command: The remainder of the command
    :return: Information regarding fiscal entities
    """
    response = rq.get("https://fr.openfisca.org/api/latest/entities")
    collect_documentation = "";
    for a in response.json():
        collect_documentation = collect_documentation + " " + response.json()[a]["documentation"];
    return "Voilà des informations sur les différentes entités fiscales en France " + collect_documentation
