# tests/test_mechanics.py
from tests.base import BaseAPITestCase


class TestMechanics(BaseAPITestCase):
    def test_create_mechanic_post(self):
        res = self.client.post(
            "/mechanics/",
            json={"name": "Grace Hopper", "email": "grace@example.com", "salary": 100000},
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.get_json())

    def test_get_mechanics_get(self):
        self.client.post("/mechanics/", json={"name": "Grace"})
        res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_update_mechanic_put(self):
        mid = self.client.post("/mechanics/", json={"name": "Grace"}).get_json()["id"]
        res = self.client.put(f"/mechanics/{mid}", json={"phone": "555-555-5555"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["phone"], "555-555-5555")

    def test_update_mechanic_not_found_negative(self):
        res = self.client.put("/mechanics/9999", json={"name": "Nope"})
        self.assertEqual(res.status_code, 404)

    def test_delete_mechanic_delete(self):
        mid = self.client.post("/mechanics/", json={"name": "Grace"}).get_json()["id"]
        res = self.client.delete(f"/mechanics/{mid}")
        self.assertEqual(res.status_code, 200)

    def test_top_mechanics_get(self):
        # Should return 200 even if empty
        res = self.client.get("/mechanics/top")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)