# from flask import Flask
# from flask_testing import TestCase
#
# from app import create_app, db
#
#
# class BaseTest(TestCase):
#     SQLALCHEMY_DATABASE_URI = "sqlite://"
#     TESTING = True
#
#     def create_app(self):
#         return create_app()
#
#     def setUp(self):
#         db.create_all()
#
#     def tearDown(self):
#
#         db.session.remove()
#         db.drop_all()

import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.DEBUG
)
