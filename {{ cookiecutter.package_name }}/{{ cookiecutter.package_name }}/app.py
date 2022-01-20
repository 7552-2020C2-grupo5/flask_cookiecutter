"""Flask api."""
import logging
from pathlib import Path

import typer
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from {{cookiecutter.package_name}}.api import api
from {{cookiecutter.package_name}}.cfg import config
from {{cookiecutter.package_name}}.models import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fix_dialect(s):
    if s.startswith("postgres://"):
        s = s.replace("postgres://", "postgresql://")
    s = s.replace("postgresql://", "postgresql+psycopg2://")
    return s


def create_app(test_db=None):
    """creates a new app instance"""
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = config.database.url(
        default=test_db or "sqlite:///{{cookiecutter.package_name}}.db", cast=fix_dialect
    )
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    new_app.config["ERROR_404_HELP"] = False
    db.init_app(new_app)
    api.init_app(new_app)
    Migrate(new_app, db, directory=Path(__file__).parent / "migrations")
    new_app.wsgi_app = ProxyFix(
        new_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1
    )  # remove after flask-restx > 0.2.0 is released
    # https://github.com/python-restx/flask-restx/issues/230
    CORS(new_app)
    return new_app

typer_app = typer.Typer()

@typer_app.command()
def run(host: str = "localhost", port: int = 5000, debug: bool = False):
    flask_app = create_app()
    flask_app.run(host=host, port=port, debug=debug)

if __name___ = "__main__":
    typer_app()
