#!/usr/bin/env python3
"""
3-app.py - Flask app with Babel setup, locale selection,
and parametrized templates
"""

from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for the user's preferred language"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """Render index.html"""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True)
