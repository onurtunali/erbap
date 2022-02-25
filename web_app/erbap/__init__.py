"""
Scifi book recommendation app:

Erbap is a distributed book recommendation engine in the genre of science fiction novels. With its substantial database and sophisticated machine learning powered recommendation system approach, it is able to pinpoint your next favorite book down to its literary tropes.

This is a very comprehensive data engineering project showcasing different technical skills such as API implementation, web scraping, data ingestion from multiple sources, task scheduling, database managing, data warehouse constructing etc.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from erbap import settings

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    if app.config["ENV"] == "development":
        cfg = settings.DevelopmentConfig()
        app.config.from_object(cfg)
    elif app.config["ENV"] == "production":
        cfg = settings.ProductionConfig()
        app.config.from_object(cfg)

    db.init_app(app)

    from erbap.main.routes import main
    from erbap.book.routes import book

    app.register_blueprint(main)
    app.register_blueprint(book)

    return app
