#!/usr/bin/env python3
import sys
import random
import json

print("Là")
with open("parametres_match.json") as json_file:
    parametres = json.load(json_file)
    print("ici")

noms_equipes = list(parametres["équipes"].keys())

random.seed()
random.shuffle(noms_equipes)

scores = { equipe : pos for pos, equipe in enumerate(noms_equipes)}

json.dump(scores, sys.stdout)
print("")
