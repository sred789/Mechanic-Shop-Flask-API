# tests/test_customers.py
from tests.base import BaseAPITestCase
from app.extensions import db
from app.models import Customer, ServiceTicket


class TestCustomers(BaseAPITestCase):
    def _create_customer_db(self, name="Ada", email="ada@example.com", password="pw"):
        with self.app.app_context():
            c = Customer(name=name, email=email, password="x")
            c.set_password(password)
            db.session.add(c)
            db.session.commit()
            return c.id

    def test_create_customer_post(self):
        res = self.client.post(
            "/customers/",
            json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "pw"},
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.get_json())

    def test_create_customer_duplicate_email_negative(self):
        self.client.post(
            "/customers/",
            json={"name": "Ada", "email": "dup@example.com", "password": "pw"},
        )
        res = self.client.post(
            "/customers/",
            json={"name": "Ada2", "email": "dup@example.com", "password": "pw"},
        )
        self.assertEqual(res.status_code, 409)

    def test_get_customers_get(self):
        self._create_customer_db()
        res = self.client.get("/customers/?page=1&per_page=10")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("items", data)

    def test_login_post(self):
        self.client.post(
            "/customers/",
            json={"name": "Ada", "email": "ada@example.com", "password": "pw"},
        )
        res = self.client.post(
            "/customers/login",
            json={"email": "ada@example.com", "password": "pw"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.get_json())

    def test_login_invalid_negative(self):
        res = self.client.post(
            "/customers/login",
            json={"email": "nope@example.com", "password": "wrong"},
        )
        self.assertEqual(res.status_code, 401)

    def test_update_customer_put(self):
        cid = self.client.post(
            "/customers/",
            json={"name": "Ada", "email": "ada@example.com", "password": "pw"},
        ).get_json()["id"]

        headers = self.auth_header_for_customer(cid)
        res = self.client.put(
            f"/customers/{cid}",
            headers=headers,
            json={"name": "Ada Updated"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["name"], "Ada Updated")

    def test_update_customer_forbidden_negative(self):
        cid = self._create_customer_db(email="ada@example.com")
        other_id = self._create_customer_db(name="Other", email="other@example.com")
        headers = self.auth_header_for_customer(other_id)

        res = self.client.put(
            f"/customers/{cid}",
            headers=headers,
            json={"name": "Hacked"},
        )
        self.assertEqual(res.status_code, 403)

    def test_delete_customer_delete(self):
        cid = self._create_customer_db(email="ada@example.com")
        headers = self.auth_header_for_customer(cid)

        res = self.client.delete(f"/customers/{cid}", headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_delete_customer_unauthorized_negative(self):
        cid = self._create_customer_db(email="ada@example.com")
        res = self.client.delete(f"/customers/{cid}")
        self.assertEqual(res.status_code, 401)

    def test_my_tickets_get(self):
        cid = self._create_customer_db(email="ada@example.com")
        with self.app.app_context():
            t = ServiceTicket(description="Oil change", vin="VIN123", status="open", customer_id=cid)
            db.session.add(t)
            db.session.commit()

        headers = self.auth_header_for_customer(cid)
        res = self.client.get("/customers/my-tickets", headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_my_tickets_unauthorized_negative(self):
        res = self.client.get("/customers/my-tickets")
        self.assertEqual(res.status_code, 401)