# -*- coding: utf-8 -*-
import unittest
from models import db, Task, Category
from app import create_app


class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_task_creation(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, 'Test Task')

    def test_category_creation(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, 'Test Category')


if __name__ == '__main__':
    unittest.main()
