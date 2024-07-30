#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config(object):
    """Config Class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/')
def home():
    """home function"""
    return render_template('6-index.html')


@babel.localeselector
def get_locale():
    """Get locale function"""
    locale = request.args.get('locale', '')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['lacale'] in app.config['LANGUAGES']:
        return g.user['locale']

    header_locale = request.headers.get('locale', '')
    if header_locale in app.config['LANGUAGES']:
        return header_locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user():
    """Get user function"""
    login_as = request.args.get('login_as')
    if login_as:
        return users.get(int(login_as))
    return None


@app.before_request
def before_request():
    """Before request function"""
    user = get_user()
    g.user = user


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
