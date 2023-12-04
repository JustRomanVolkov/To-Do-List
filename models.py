# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#     Связующая таблица для связи многие-ко-многим между задачами (Task) и категориями (Category).
task_categories = db.Table('task_categories',
                           db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                           db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                           )


class Task(db.Model):
    """
    Класс, представляющий задачу.

    Attributes:
        id (int): Уникальный идентификатор задачи (первичный ключ).
        title (str): Заголовок задачи (не может быть пустым).
        description (str): Описание задачи.
        date_created (datetime): Дата и время создания задачи (по умолчанию текущее время).
        file_path (str): Путь к файлу, связанному с задачей.
        categories (list): Список категорий, к которым принадлежит задача.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(300))  # Путь к файлу
    categories = db.relationship('Category', secondary=task_categories, lazy='subquery',
                                 backref=db.backref('tasks', lazy=True))


class Category(db.Model):
    """
    Класс, представляющий категорию задачи.

    Attributes:
        id (int): Уникальный идентификатор категории (первичный ключ).
        name (str): Наименование категории задачи (не может быть пустым).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
