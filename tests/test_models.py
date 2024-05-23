# -*- coding: utf-8 -*-
import unittest
from todo_app.models import db, Task, Category
from app import create_app


class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app('todo_app.config.TestConfig')
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

    def test_task_category_association(self):
        task = Task(title='Test Task', description='Test Description')
        category = Category(name='Test Category')
        task.categories.append(category)
        db.session.add(task)
        db.session.commit()

        self.assertEqual(len(task.categories), 1)
        self.assertEqual(task.categories[0].name, 'Test Category')

    def test_task_deletion(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()

        db.session.delete(task)
        db.session.commit()

        self.assertIsNone(db.session.get(Task, task.id))

    def test_task_update(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()

        task.title = 'Updated Task'
        db.session.commit()

        self.assertEqual(task.title, 'Updated Task')

    def test_category_update(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        category.name = 'Updated Category'
        db.session.commit()

        self.assertEqual(category.name, 'Updated Category')

    def test_category_deletion(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        db.session.delete(category)
        db.session.commit()

        self.assertIsNone(db.session.get(Category, category.id))

    def test_task_validation(self):
        with self.assertRaises(ValueError):
            task = Task(title='', description='Test Description')
            db.session.add(task)
            db.session.commit()

    def test_category_validation(self):
        with self.assertRaises(ValueError):
            category = Category(name='')
            db.session.add(category)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
