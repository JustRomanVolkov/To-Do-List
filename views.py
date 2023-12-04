# -*- coding: utf-8 -*-

import os

from flask import Blueprint, current_app, request, jsonify, make_response
from sqlalchemy.orm import Session
from models import db, Category, Task
from services import handle_categories, handle_file_upload

# Создание объекта tasks_blueprint для маршрутов и представлений, связанных с задачами в приложении Flask
tasks_blueprint = Blueprint('tasks', __name__)


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
        'date_created': task.date_created.isoformat() if task.date_created else None,
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


@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    """
    Создает новую задачу.

    Returns:
        json: JSON-ответ с сообщением о создании задачи и ее идентификатором или ошибкой в случае неверных данных.
    """

    data = request.get_json()
    # Валидация данных
    if not data or 'title' not in data or 'description' not in data or 'categories' not in data:
        return jsonify({'message': 'Missing data'}), 400

    new_task = Task(
        title=data['title'],
        description=data['description']
    )

    # Обработка категорий
    handle_categories(data['categories'], new_task)

    # Обработка файла
    file_path = handle_file_upload(request, current_app.config['UPLOAD_FOLDER'])
    if file_path:
        new_task.file_path = file_path

    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully', 'id': new_task.id}), 201


@tasks_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    category_filter = request.args.get('category')
    sort_by = request.args.get('sort', 'date_created')
    order = request.args.get('order', 'asc')

    query = Task.query

    # Фильтрация по категориям
    if category_filter:
        query = query.join(Task.categories).filter(Category.name == category_filter)

    # Сортировка
    if sort_by and hasattr(Task, sort_by):
        if order == 'desc':
            query = query.order_by(db.desc(getattr(Task, sort_by)))
        else:
            query = query.order_by(getattr(Task, sort_by))

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
    session = Session(bind=db.engine)
    task = session.get(Task, id)
    if task:
        task_data = task_to_dict(task)
        return jsonify({'task': task_data})
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

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    task = Task.query.get(id)
    if not task:
        return make_response('Task not found', 404)

    title = data.get('title')
    description = data.get('description')
    categories = data.get('categories')

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    if categories is not None:
        handle_categories(categories, task)

    file_path = handle_file_upload(request, current_app.config['UPLOAD_FOLDER'])
    if file_path:
        task.file_path = file_path

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})


@tasks_blueprint.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    """
    Удаляет задачу по её идентификатору.

    Args:
        id (int): Идентификатор задачи.

    Returns:
        json: JSON-ответ с сообщением об успешном удалении задачи и связанного файла.
    """
    task = Task.query.get(id)
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
    category = Category.query.get(id)
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
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    return make_response('Category not found', 404)
