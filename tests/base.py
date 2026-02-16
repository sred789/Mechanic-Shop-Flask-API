# tests/base.py
import unittest

from app import create_app
from app.extensions import db
from app.utils.token import encode_token


class BaseAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
            })


        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def auth_header_for_customer(self, customer_id: int) -> dict:
        with self.app.app_context():
            token = encode_token(customer_id)
        return {"Authorization": f"Bearer {token}"}