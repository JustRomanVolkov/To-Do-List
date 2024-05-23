# -*- coding: utf-8 -*-
import unittest
import json
from app import create_app
from todo_app.models import db, Task, Category


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('todo_app.config.TestConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Добавление категории "General" в базу данных для тестирования
        general_category = Category(name='General')
        db.session.add(general_category)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_task(self):
        response = self.client.post('/tasks', json={'title': 'New Task', 'description': 'Test description',
                                                    'categories': ['General']})
        self.assertEqual(response.status_code, 201, f"Response body: {response.data}")

    def test_get_task(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        response = self.client.get(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        # Создание задачи для обновления
        task = Task(title='Old Task', description='Old Description')
        db.session.add(task)
        db.session.commit()

        # Обновление задачи
        response = self.client.put(f'/tasks/{task.id}',
                                   json={'title': 'Updated Task', 'description': 'Updated Description',
                                         'categories': ['General']})
        self.assertEqual(response.status_code, 200)

        # Получение обновленной задачи
        response = self.client.get(f'/tasks/{task.id}')
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Task')
        self.assertEqual(data['description'], 'Updated Description')

    def test_delete_task(self):
        # Создание задачи для удаления
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()

        # Удаление задачи
        response = self.client.delete(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)

        # Проверка, что задача удалена
        response = self.client.get(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 404)

    def test_get_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('General', [category['name'] for category in data['categories']])

    def test_get_category(self):
        category = Category(name='SpecificCategory')
        db.session.add(category)
        db.session.commit()

        response = self.client.get(f'/categories/{category.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['category']['name'], 'SpecificCategory')

    def test_create_category(self):
        response = self.client.post('/categories', json={'name': 'NewCategory'})
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/categories')
        data = json.loads(response.data)
        self.assertIn('NewCategory', [category['name'] for category in data['categories']])

    def test_delete_category(self):
        category = Category(name='ToDeleteCategory')
        db.session.add(category)
        db.session.commit()

        response = self.client.delete(f'/categories/{category.id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/categories/{category.id}')
        self.assertEqual(response.status_code, 404)

    def test_create_task_without_title(self):
        response = self.client.post('/tasks', json={'description': 'Test description', 'categories': ['General']})
        self.assertEqual(response.status_code, 400, f"Response body: {response.data}")

    def test_create_task_with_long_description(self):
        response = self.client.post('/tasks', json={'title': 'New Task', 'description': 'a' * 201, 'categories': ['General']})
        self.assertEqual(response.status_code, 400, f"Response body: {response.data}")


if __name__ == '__main__':
    unittest.main()
