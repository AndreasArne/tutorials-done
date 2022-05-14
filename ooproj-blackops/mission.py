from sqlalchemy import Column, String, Integer, Float, Boolean, PickleType
from base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Mission(Base):

    __tablename__ = "mission"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lost = Column(Boolean)
    result = Column(PickleType)
    # heroes = relationship("Character")
    # villains = relationship("Character")

    def __init__(self, name,  villains):
        self.name = name
        self.villains = villains
        self.lost = False
        self.heroes = []
        self.result = {}

    def get_display_dict(self):
        return {
        "name": self.name,
        "villains": self.villains,
        "heroes": self.heroes,
        "result": self.result
        }

    def fight(self, villain, hero):
        while not villain.caught and not hero.caught:
            if hero.attack(villain):
                return 1
            # print("{}´s hp is {} after {} punched him".format(villain.name, villain.hp, hero.name))
            if villain.attack(hero):
                return 2
            # print("{}´s hp is {} after {} punched him".format(hero.name, hero.hp, villain.name))

    def start_fight(self):
        villain_count = 0
        hero_count = 0
        while villain_count < len(self.villains) and not self.lost:
            villain = self.villains[villain_count]
            hero = self.heroes[hero_count]
            count = hero_count + villain_count + 1
            print("Round {}!\n{} vs {}".format(count, hero.name, villain.name))

            if self.fight(villain, hero) == 1:
                villain_count += 1
            else:
                hero_count += 1
                if hero_count == len(self.heroes):
                    self.lost = True

    def start_mission(self):
        print("Begin mission {}!".format(self.name))
        self.start_fight()
        self.calc_result()
        return self.result

    def calc_result(self):
        if self.lost:
            self.result["res"] = False
            self.result["caught"] = [hero.name for hero in self.heroes] 
        else:
            self.result["res"] = True
            self.result["caught"] = [vill.name for vill in self.villains]
