from unittest import mock
from unittest.mock import PropertyMock, Mock

from workout_tests.bootstrap import BaseTestCase, User


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

    @mock.patch.object(User, "query", new_callable=PropertyMock)
    def test_edit_user_with_error(self, mock_obj):
        new_data = {
            "first_name": "Testing",
            "last_name": "User Application"
        }

        mock_obj.return_value.filter.side_effect = [Mock(autospec=True), self.raise_exception]

        result = self.client.post(f"/users/{self._auth_user.id}", json=new_data)

        self.assert500(result)
