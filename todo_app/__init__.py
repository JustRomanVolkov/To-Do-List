# -*- coding: utf-8 -*-

from flask import Flask
from .config import Config
from .extensions import db, migrate
from .views import tasks_blueprint


def create_app(config_class=Config):
    """
    Создает и настраивает Flask-приложение.

    Args:
        config_class: Класс конфигурации для настройки приложения.

    Returns:
        Flask: Экземпляр Flask-приложения.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_blueprint)

    with app.app_context():
        db.create_all()

    return app
