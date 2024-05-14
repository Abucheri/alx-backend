#!/usr/bin/env python3
"""
1-app.py - Basic Flask app with Babel setup
"""

from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


@app.route('/')
def index():
    """Render index.html"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(debug=True)
