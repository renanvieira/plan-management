from workout_management.extensions import db_context
from workout_management.models import User
from workout_tests.bootstrap import BaseTestCase


class UserCreationTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(UserCreationTestCase, self).setUp()

    def tearDown(self):
        super(UserCreationTestCase, self).tearDown()

    def test_create_user(self):
        signup_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "user@test.com",
            "birth_date": "1990-11-21",
            "password": "123$456#"
        }

        result = self.client.post("/users", json=signup_data)

        self.assert200(result, result.data.decode("utf-8"))
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertNotIn("password", result.json)

    def test_create_user_without_name(self):
        signup_data = {
            "email": "user@test.com",
            "birth_date": "1990-11-21",
            "password": "123$456#"
        }

        result = self.client.post("/users", json=signup_data)

        self.assert400(result, result.data.decode("utf-8"))

    def test_create_users_with_same_email(self):
        signup_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "user@test.com",
            "birth_date": "1990-11-21",
            "password": "123$456#"
        }

        result1 = self.client.post("/users", json=signup_data)

        self.assert200(result1, result1.data.decode("utf-8"))
        self.assertIsNotNone(result1.json)

        signup_data = {
            "first_name": "Test 2",
            "last_name": "User 2",
            "email": "user@test.com",
            "birth_date": "1992-11-21",
            "password": "789#321@"
        }

        result2 = self.client.post("/users", json=signup_data)

        self.assert400(result2, result2.data.decode("utf-8"))
