import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

import app.main as main
from app.db.store import FeedzStore


class TestApiHardening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.store = FeedzStore(f"sqlite:///{Path(cls.tempdir.name) / 'test.db'}")
        main.store = cls.store
        cls.client = TestClient(main.app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)
        cls.store.engine.dispose()
        cls.tempdir.cleanup()

    def test_register_login_and_me(self):
        registered = self.client.post(
            "/api/auth/register",
            json={"identifier": "person@example.com", "password": "longsecurepassword", "name": "Test Person"},
        )
        self.assertEqual(registered.status_code, 201)
        token = registered.json()["access_token"]

        me = self.client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["identifier"], "person@example.com")

        login = self.client.post(
            "/api/auth/login",
            json={"identifier": "person@example.com", "password": "wrong-password"},
        )
        self.assertEqual(login.status_code, 401)

    def test_feed_requires_authentication(self):
        response = self.client.get("/api/feed")
        self.assertEqual(response.status_code, 401)

    def test_users_are_isolated(self):
        first = self.client.post(
            "/api/auth/register",
            json={"identifier": "first@example.com", "password": "longsecurepassword", "name": "First"},
        )
        second = self.client.post(
            "/api/auth/register",
            json={"identifier": "second@example.com", "password": "longsecurepassword", "name": "Second"},
        )
        first_token = first.json()["access_token"]
        second_token = second.json()["access_token"]

        held = self.client.post(
            "/api/portfolio/holding",
            headers={"Authorization": f"Bearer {first_token}"},
            json={"symbol": "HDFCBANK", "weight": 100, "quantity": 10, "avg_price": 1600},
        )
        self.assertEqual(held.status_code, 200)

        second_me = self.client.get("/api/me", headers={"Authorization": f"Bearer {second_token}"})
        self.assertEqual(second_me.json()["holdings"], [])

    def test_validation_and_health(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        invalid = self.client.post(
            "/api/auth/register",
            json={"identifier": "x", "password": "short", "name": ""},
        )
        self.assertEqual(invalid.status_code, 422)
        self.assertEqual(invalid.json()["error"], "validation_error")


if __name__ == "__main__":
    unittest.main(verbosity=2)
