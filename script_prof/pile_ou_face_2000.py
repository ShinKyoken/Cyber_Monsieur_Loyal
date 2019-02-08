#!/usr/bin/env python3
import sys
import random
import json


parametres = json.load(sys.argv[1])
noms_equipes = list(parametres["equipes"].keys())

random.seed()
random.shuffle(noms_equipes)

scores = { equipe : pos for pos, equipe in enumerate(noms_equipes)}
json.dump(scores, sys.stdout)
print("")
