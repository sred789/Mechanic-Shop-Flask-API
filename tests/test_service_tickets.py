# tests/test_service_tickets.py
from tests.base import BaseAPITestCase


class TestServiceTickets(BaseAPITestCase):
    def _seed_customer(self):
        return self.client.post(
            "/customers/",
            json={"name": "Ada", "email": "ada@example.com", "password": "pw"},
        ).get_json()["id"]

    def _seed_mechanic(self):
        return self.client.post("/mechanics/", json={"name": "Grace"}).get_json()["id"]

    def _seed_part(self):
        return self.client.post("/inventory/", json={"name": "Brake Pads", "price": 49.99}).get_json()["id"]

    def _seed_ticket(self, customer_id):
        return self.client.post(
            "/service-tickets/",
            json={"description": "Oil change", "vin": "VIN123", "status": "open", "customer_id": customer_id},
        ).get_json()["id"]

    def test_create_ticket_post(self):
        cid = self._seed_customer()
        res = self.client.post(
            "/service-tickets/",
            json={"description": "Brake job", "vin": "VIN999", "customer_id": cid},
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.get_json())

    def test_get_tickets_get(self):
        cid = self._seed_customer()
        self._seed_ticket(cid)
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_assign_mechanic_put(self):
        cid = self._seed_customer()
        tid = self._seed_ticket(cid)
        mid = self._seed_mechanic()

        res = self.client.put(f"/service-tickets/{tid}/assign-mechanic/{mid}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(mid, res.get_json().get("mechanic_ids", []))

    def test_remove_mechanic_put(self):
        cid = self._seed_customer()
        tid = self._seed_ticket(cid)
        mid = self._seed_mechanic()
        self.client.put(f"/service-tickets/{tid}/assign-mechanic/{mid}")

        res = self.client.put(f"/service-tickets/{tid}/remove-mechanic/{mid}")
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(mid, res.get_json().get("mechanic_ids", []))

    def test_edit_ticket_put(self):
        cid = self._seed_customer()
        tid = self._seed_ticket(cid)
        res = self.client.put(f"/service-tickets/{tid}/edit", json={"status": "closed"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "closed")

    def test_add_part_put(self):
        cid = self._seed_customer()
        tid = self._seed_ticket(cid)
        pid = self._seed_part()

        res = self.client.put(f"/service-tickets/{tid}/add-part/{pid}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(pid, res.get_json().get("part_ids", []))

    def test_assign_mechanic_not_found_negative(self):
        res = self.client.put("/service-tickets/9999/assign-mechanic/9999")
        self.assertEqual(res.status_code, 404)