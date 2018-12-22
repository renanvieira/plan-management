from time import sleep

from flask import app

from workout_tests.bootstrap import BaseTestCase


class UserDeletionTestCase(BaseTestCase):
    def setUp(self, **kwargs):
        super(UserDeletionTestCase, self).setUp()

        self.user = self.create_user()

    def tearDown(self):
        super(UserDeletionTestCase, self).tearDown()

    def test_edit_user(self):
        new_data = {
            "first_name": "Testing",
            "last_name": "User Application"
        }

        result = self.client.post(f"/users/{self._auth_user.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["first_name"], "Testing")
        self.assertIn(result.json["last_name"], "User Application")

    def test_edit_user_with_invalid_data(self):
        new_data = {
            "birth_date": "abc",
        }

        result = self.client.post(f"/users/{self._auth_user.id}", json=new_data)

        self.assert400(result)

    def test_edit_inexistent_user(self):
        new_data = {
            "first_name": "Testing 2",
            "last_name": "User Application 2"
        }

        result = self.client.post(f"/users/999999", json=new_data)

        self.assert404(result)

    def test_edit_user_password(self):
        new_data = {
            "password": "abc$123",
        }

        result = self.client.post(f"/users/{self._auth_user.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        # TODO: validate password after login implementation

    def test_edit_user_differente_from_authenticated(self):
        new_data = {
            "first_name": "Testing",
            "last_name": "User Application"
        }

        result = self.client.post(f"/users/{self.user.id}", json=new_data)

        self.assert403(result)