# -*- coding: utf-8 -*-
import os
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from .extensions import db
from .models import Category


def allowed_file(filename):
    """
    Проверяет, разрешено ли загружать файл с данным расширением.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: True, если файл с указанным расширением разрешен, иначе False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}


def handle_file_upload(request, upload_folder):
    """
    Обрабатывает загрузку файла и сохраняет его в указанную папку.

    Args:
        request (Request): Запрос Flask, содержащий файл.
        upload_folder (str): Путь к папке, в которую нужно сохранить файл.

    Returns:
        str or None: Путь к сохраненному файлу, если файл успешно загружен и сохранен, иначе None.
    """
    if 'file' in request.files:
        file_storage = request.files['file']
        if file_storage and allowed_file(file_storage.filename):
            filename = secure_filename(file_storage.filename)
            file_path = os.path.join(upload_folder, filename)
            file_storage.save(file_path)
            return file_path
    return None


def handle_categories(category_names, task):
    """
    Обрабатывает категории для задачи, создавая новые категории, если они не существуют,
    и добавляя их к задаче.

    Args:
        category_names (list of str): Список названий категорий.
        task (Task): Задача, к которой нужно добавить категории.
    """
    for category_name in category_names:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
        if category not in task.categories:
            task.categories.append(category)


def task_to_dict(task):
    """
    Преобразует объект задачи в словарь для сериализации в JSON.

    Args:
        task (Task): Объект задачи.

    Returns:
        dict: Словарь с данными о задаче.
    """
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat() if task.created_at else None,
        'updated_at': task.updated_at.isoformat() if task.updated_at else None,
        'file_path': task.file_path,
        'categories': [category.name for category in task.categories]
    }


def category_to_dict(category):
    """
    Преобразует объект категории в словарь для сериализации в JSON.

    Args:
        category (Category): Объект категории.

    Returns:
        dict: Словарь с данными о категории.
    """
    return {'id': category.id, 'name': category.name}


def validate_task_data(data):
    if not data:
        raise BadRequest('No input data provided')
    if 'title' not in data or not data['title']:
        raise BadRequest('Title is required')
    if 'description' in data and len(data['description']) > 200:
        raise BadRequest('Description is too long')
