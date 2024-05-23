# -*- coding: utf-8 -*-

import os
from flask import Blueprint, current_app, request, jsonify, make_response
from .models import Category, Task
from .extensions import db
from .services import (handle_categories,
                                   handle_file_upload,
                                   task_to_dict,
                                   category_to_dict,
                                   validate_task_data)

# Создание объекта tasks_blueprint для маршрутов и представлений, связанных с задачами в приложении Flask
tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    """
    Создает новую задачу.

    Returns:
        json: JSON-ответ с сообщением о создании задачи и ее идентификатором или ошибкой в случае неверных данных.
    """

    data = request.get_json()
    validate_task_data(data)

    new_task = Task(
        title=data['title'],
        description=data.get('description')
    )

    # Обработка категорий
    handle_categories(data.get('categories', []), new_task)

    # Обработка файла
    file_path = handle_file_upload(request, current_app.config['UPLOAD_FOLDER'])
    if file_path:
        new_task.file_path = file_path

    db.session.add(new_task)
    db.session.commit()
    return jsonify(task_to_dict(new_task)), 201


@tasks_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    category_filter = request.args.get('category')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'asc')

    query = Task.query

    # Фильтрация по категориям
    if category_filter:
        query = query.join(Task.categories).filter(Category.name == category_filter)

    # Сортировка
    if hasattr(Task, sort_by):
        query = query.order_by(getattr(Task, sort_by).desc() if order == 'desc' else getattr(Task, sort_by))

    # Ограничение на количество результатов
    tasks = query.limit(100).all()

    # Преобразование задач в список словарей
    tasks_data = [task_to_dict(task) for task in tasks]

    return jsonify({'tasks': tasks_data})


@tasks_blueprint.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    """
    Возвращает список задач с возможностью фильтрации и сортировки.

    Returns:
        json: JSON-ответ с списком задач.
    """
    task = db.session.get(Task, id)
    if task:
        return jsonify(task_to_dict(task))
    return make_response('Task not found', 404)


@tasks_blueprint.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    """
    Обновляет существующую задачу.

    Args:
        id (int): Идентификатор задачи.

    Returns:
        json: JSON-ответ с сообщением об успешном обновлении.
    """
    data = request.get_json()
    validate_task_data(data)

    task = db.session.get(Task, id)
    if not task:
        return make_response('Task not found', 404)

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    handle_categories(data.get('categories', []), task)
    file_path = handle_file_upload(request, current_app.config['UPLOAD_FOLDER'])
    if file_path:
        task.file_path = file_path

    db.session.commit()
    return jsonify(task_to_dict(task))


@tasks_blueprint.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    """
    Удаляет задачу по её идентификатору.

    Args:
        id (int): Идентификатор задачи.

    Returns:
        json: JSON-ответ с сообщением об успешном удалении задачи и связанного файла.
    """
    task = db.session.get(Task, id)
    if task:
        if task.file_path and os.path.exists(task.file_path):
            os.remove(task.file_path)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task and associated file deleted successfully'})
    return make_response('Task not found', 404)


@tasks_blueprint.route('/categories', methods=['GET'])
def get_categories():
    """
    Возвращает список всех категорий.

    Returns:
        json: JSON-ответ с списком категорий.
    """
    categories = Category.query.all()
    categories_data = [category_to_dict(category) for category in categories]
    return jsonify({'categories': categories_data})


@tasks_blueprint.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    """
    Возвращает список всех категорий.

    Returns:
        json: JSON-ответ с данными о категориях.
    """
    category = db.session.get(Category, id)
    if category:
        return jsonify({'category': {'id': category.id, 'name': category.name}})
    return make_response('Category not found', 404)


@tasks_blueprint.route('/categories', methods=['POST'])
def create_category():
    """
    Создает новую категорию.

    Returns:
        json: JSON-ответ с сообщением об успешном создании и данными о категории.
    """
    data = request.get_json()

    # Валидация данных
    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully',
                    'category': {'id': new_category.id, 'name': new_category.name}}), 201


@tasks_blueprint.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    """
    Удаляет категорию по её идентификатору.

    Args:
        id (int): Идентификатор категории.

    Returns:
        json: JSON-ответ с сообщением об успешном удалении категории.
    """
    category = db.session.get(Category, id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    return make_response('Category not found', 404)
