# -*- coding: utf-8 -*-

from flask import Flask
from models import db
from config import Config
from views import tasks_blueprint


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

    with app.app_context():
        db.create_all()

    app.register_blueprint(tasks_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
