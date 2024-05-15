#!/usr/bin/env python3
"""
7-app.py - Flask app with Babel setup, locale selection,
time zone inference, and user login emulation
"""

from flask import Flask, render_template, g, request
from flask_babel import Babel
import pytz


app = Flask(__name__)
babel = Babel(app)


# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for the user's preferred language"""
    # Check if locale is provided in URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Check if user is logged in and has preferred locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # Fallback to request's accept languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Determine the best match for the user's preferred time zone"""

    # Check if timezone is provided in URL parameters
    tz = request.args.get('timezone')
    if tz:
        try:
            pytz.timezone(tz)
            return tz
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Check if user is logged in and has preferred timezone
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user.get('timezone'))
            return g.user.get('timezone')
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Fallback to UTC
    return "UTC"


@app.route('/')
def index() -> str:
    """Render index.html"""
    return render_template('7-index.html')


def get_user(user_id: int) -> dict:
    """Get user info by user ID"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Set current user in global g object"""
    user_id = int(request.args.get('login_as', 0))
    g.user = get_user(user_id)


if __name__ == "__main__":
    app.run(debug=True)
