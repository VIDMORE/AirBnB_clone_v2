#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask, escape, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    """Function that diplays Hello HBNB"""

    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_hbnb():
    """Function that diplays HBNB"""

    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Function that displays “C ” followed by a string"""

    text = escape(text)
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """Function that displays “Python ” followed by a string"""

    text = escape(text)
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Function that displays a number “# ”"""

    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    """Function that displays a number in a template"""

    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
