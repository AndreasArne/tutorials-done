#!/usr/bin/env python3
from character import Character
from mission import Mission

bStats = {"hp": 100, "defense": 20, "dmg": 10, "catch_rate": 70}
gStats = {"hp": 130, "defense": 20, "dmg": 10, "catch_rate": 30}
jStats = {"hp": 100, "defense": 40, "dmg": 10, "catch_rate": 80}
uStats = {"hp": 120, "defense": 30, "dmg": 10, "catch_rate": 40}
batman = Character("batman", bStats)
greenLantern = Character("green lantern", bStats)
joker = Character("joker", jStats)
universe = Character("univers", uStats)

mission = Mission("Death squad", [joker, universe])
mission.heroes.append(batman)
mission.heroes.append(greenLantern)
mission.start_mission()
print("j hp: " + str(joker.hp))
print("u hp: " + str(universe.hp))
print("b hp: " + str(batman.hp))
print("g hp: " + str(greenLantern.hp))

