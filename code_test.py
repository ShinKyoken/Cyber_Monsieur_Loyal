#!/usr/bin/env python3
import sys
import random
import json


with open("parametres.json") as json_file:
    parametres = json.load(json_file)

noms_equipes = list(parametres["equipes"].keys())
idPartie = parametres["idPartie"]

random.seed()
random.shuffle(noms_equipes)

scores ={ "equipes" :
         { equipe : pos for pos, equipe in enumerate(noms_equipes)},
         "idPartie" : idPartie
        }

json.dump(scores, sys.stdout, indent=4)
