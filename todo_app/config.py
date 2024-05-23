# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    if os.getenv('LOCAL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
