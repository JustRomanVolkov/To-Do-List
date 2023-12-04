# -*- coding: utf-8 -*-
import os
from werkzeug.utils import secure_filename
from models import db, Category


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
