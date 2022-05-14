from character import Character
from mission import Mission
from base import Base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from flask import request
import random


class Controller():
    engine = create_engine("sqlite:///db/blackops.sqlite",  connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self):
        self.heroes = []
        self.villains = []
        self.av_villains = []
        self.missions = []
        self.current_mission = -1
        self.read_db()

    def create_hero(self, name, stats):
        heroe = Character(name, stats)
        self.session.add(heroe)
        self.session.commit()
        self.heroes.append(heroe)

    def create_villain(self, name, stats):
        villain = Character(name, stats)
        self.session.add(villain)
        self.session.commit()
        self.villains.append(villain)
        self.av_villains.append(villain)

        # self.villains.append(Character(name, stats))
        # mis = Mission("Black desert", self.villains)
        # self.session.add(mis)
        # self.missions.append(mis)
        # self.session.commit()
        # ll = self.alchemyToObjectList(self.session.query(Mission))
        # print(ll[0].villains[0].name)

    def add_heroes_mission(self):
        miss = self.get_mission(request.form["mission"])
        for h in self.heroes:
            try:
                if request.form[h.name]:
                    miss.heroes.append(h)
            except:
                pass
        # self.session.commit()

    def start_fight(self, mission_name):
        self.get_mission(mission_name).start_mission()

    def create_mission(self, name):
        nr = random.randint(1, len(self.av_villains))
        nr = nr - 1 if nr > 3 else nr
        vl = []
        for x in range(nr):
            indx = random.randint(1, len(self.av_villains)) -1
            vl.append(self.av_villains.pop(indx))

        miss = Mission(name, vl)
        # self.session.add(miss)
        # self.session.commit()
        self.missions.append(miss)

    def get_all_missions_dicts(self):
        return list(map(Mission.get_display_dict, self.missions))
        # ll = []
        # for x in self.missions:
        #     ll.append(x.get_display_dict())
        # return ll

    def get_mission(self, name):
        for miss in self.missions:
            if miss.name == name:
                return miss

    def get_mission_dict(self, name):
        return self.get_mission(name).get_display_dict()

    def drop_all_tables(self):
        Base.metadata.drop_all(self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

    def rollback(self):
        self.session.rollback()

    def read_db(self):
        self.missions = self.alchemyToObjectList(self.session.query(Mission))
        self.load_characters(self.session.query(Character))

    def load_characters(self, chars):
        chars = self.alchemyToObjectList(chars)
        for char in chars:
            if char.evil:
                self.villains.append(char)
                t = False
                for m in self.missions:
                    for c in m.villains:
                        if char.name == c.name:
                            t = True
                            break
                if not t:
                    self.av_villains.append(char)
            else:
                self.heroes.append(char)

    @staticmethod
    def alchemyToObjectList(query):
        newList = [x for x in query]
        return newList
