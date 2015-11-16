from json import load, dumps
from random import sample

from flask import Flask, Response, request
from six.moves import zip

app = Flask(__name__)

with open("henchmen.json", "rb") as infile:
    henchmen = load(infile)
with open("heroes.json", "rb") as infile:
    heroes = load(infile)
with open("masterminds.json", "rb") as infile:
    masterminds = load(infile)
with open("villains.json", "rb") as infile:
    villains = load(infile)
with open("card_counts.json", "rb") as infile:
    card_counts = load(infile)


card_types = ["villains", "henchmen", "heroes", "masterminds"]
all_choices = [villains, henchmen, heroes, masterminds]


@app.route('/get_random')
def run_rng():
    n_players = request.args.get("n")
    if n_players is None:
        return Response("number of players (n) not specified")
    try:
        n_players = int(n_players)
    except ValueError:
        return Response("number of players must be an integer",
                        status=400)
    if n_players < 2 or n_players > 5:
        return Response("number of players must be between 2 and 5",
                        status=400)
    results = {}
    for count, card_type, choices in \
            zip(card_counts[str(n_players)], card_types, all_choices):
        results[card_type] = sample(choices, count)
    return Response(dumps(results), mimetype="application/json")


@app.route('/')
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
