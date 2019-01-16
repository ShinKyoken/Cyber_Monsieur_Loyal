#!/usr/bin/env python3
import sys
import random
import json


equipes = json.load(sys.stdin)
noms_equipes = list(equipes.keys())

random.shuffle(noms_equipes)

scores = { equipe : pos for pos, equipe in enumerate(noms_equipes)}

json.dump(scores, sys.stdout)
print("")
