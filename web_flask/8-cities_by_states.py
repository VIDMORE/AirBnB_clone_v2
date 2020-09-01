#!/usr/bin/python3
"""This module starts a Flask web application and displays states
"""
from flask import Flask, escape, render_template
from models import storage
from models import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def display_states():
    """Function that displays states"""

    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(self):
    """Function that removes the current SQLAlchemy Session"""

    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def city_state_list():
    """Function to render states from storage"""

    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
