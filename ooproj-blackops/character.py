#!/usr/bin/env python3
import random
from sqlalchemy import Column, String, Integer, Float, Boolean
from base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from mission import Mission


class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Float)
    defense = Column(Integer)
    dmg = Column(Integer)
    catch_rate = Column(Integer)
    caught = Column(Boolean)
    evil = Column(Boolean)
    mission_id = Column(Integer, ForeignKey('mission.id'))

    mission_h = relationship("Mission", backref="heroes")#backref="heroes"
    mission_v = relationship("Mission", backref="villains")#back_populates="villains"

    def __init__(self, name, stats):
        self.name = name
        for key, val in stats.items():
            setattr(self, key, val)
        self.caught = False

    def attack(self, enemy):
        if random.randint(0, self.catch_rate) > enemy.hp:
            print(enemy.name + " got caught!")
            enemy.caught = True
            return True
        else:
            enemy.hp -= self.calc_dmg(enemy)
            return False

    def calc_dmg(self, enemy):
        return self.dmg * (1 - enemy.defense/100)
