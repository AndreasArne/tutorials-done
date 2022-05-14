#!/usr/bin/env python3
"""
My first Flask app
"""
from flask import Flask, render_template
from flask import request, redirect
from controller import Controller


app = Flask(__name__)
controller = Controller()
# controller.read_db()

@app.route("/", methods=["GET"])
def main():
    """
    index
    """
    return render_template("index.html", characters=controller.heroes, missions=controller.get_all_missions_dicts())

@app.route("/setup_mission", methods=["GET"])
def setup_mission():
    """
    config shit up
    """ 
    mission = controller.get_mission_dict(request.args.get("name"))
    return render_template("config_mission.html", mission=mission, characters=controller.heroes, villains=mission["villains"])

@app.route("/start/mission", methods=["POST"])
def start_mission():
    controller.add_heroes_mission()
    controller.start_fight(request.form["mission"])
    return redirect("/show/mission?name={}".format(request.form["mission"]))

@app.route("/show/mission")
def show_mission():
    mission = controller.get_mission_dict(request.args.get("name"))
    return render_template("show_mission.html", mission=mission, villains=mission["villains"], characters=mission["heroes"])

@app.route("/create/hero", methods=["GET"])
def create_hero():
    """
    about
    """
    return render_template("create_hero.html", characters=controller.heroes, c_type="hero")

@app.route("/create/villain", methods=["GET"])
def create_villain():
    """
    about
    """
    return render_template("create_villain.html", characters=controller.villains, c_type="villain")

@app.route("/create/mission", methods=["GET"])
def create_mission():
    """
    about
    """
    missions=controller.get_all_missions_dicts()
    return render_template("create_mission.html", missions=missions, av=len(controller.av_villains))

@app.route("/add/hero", methods=["POST"])
def add_hero():
    """
    Create a hero
    """
    stats = {
        "hp": request.form["hp"],
        "defense": request.form["defense"],
        "dmg": request.form["dmg"],
        "catch_rate": request.form["catch_rate"],
        "evil": 0
    }
    controller.create_hero(request.form["name"], stats)
    return redirect("/create/hero")

@app.route("/add/villain", methods=["POST"])
def add_villain():
    """
    Create a villain
    """
    stats = {
        "hp": request.form["hp"],
        "defense": request.form["defense"],
        "dmg": request.form["dmg"],
        "catch_rate": request.form["catch_rate"],
        "evil": 1
    }
    controller.create_villain(request.form["name"], stats)
    return redirect("/create/villain")

@app.route("/add/mission", methods=["POST"])
def add_mission():
    """
    Create a mission
    """
    controller.create_mission(request.form["name"])
    return redirect("/create/mission")

@app.route("/drop/all_tables", methods=["GET"])
def drop_all_tables():
    controller.drop_all_tables()
    return redirect("/")

@app.route("/create/all_tables", methods=["GET"])
def create_all_tables():
    controller.create_all_tables()
    return redirect("/")

@app.route("/rollback", methods=["GET"])
def rollback():
    controller.rollback()
    return redirect("/")


if __name__ == "__main__":
    """
    main run
    """
    app.run(debug=True)
