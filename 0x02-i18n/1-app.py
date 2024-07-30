#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, render_template
from flask_babel import Babel

class Config:
    """Config Class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def home():
    """home function"""
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
