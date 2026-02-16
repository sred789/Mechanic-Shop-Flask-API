# tests/test_inventory.py
from tests.base import BaseAPITestCase


class TestInventory(BaseAPITestCase):
    def test_create_part_post(self):
        res = self.client.post("/inventory/", json={"name": "Brake Pads", "price": 49.99})
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.get_json())

    def test_get_parts_get(self):
        self.client.post("/inventory/", json={"name": "Brake Pads", "price": 49.99})
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_update_part_put(self):
        pid = self.client.post("/inventory/", json={"name": "Pads", "price": 10}).get_json()["id"]
        res = self.client.put(f"/inventory/{pid}", json={"price": 12.5})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(float(res.get_json()["price"]), 12.5)

    def test_delete_part_delete(self):
        pid = self.client.post("/inventory/", json={"name": "Pads", "price": 10}).get_json()["id"]
        res = self.client.delete(f"/inventory/{pid}")
        self.assertEqual(res.status_code, 200)

    def test_update_part_not_found_negative(self):
        res = self.client.put("/inventory/9999", json={"price": 1})
        self.assertEqual(res.status_code, 404)