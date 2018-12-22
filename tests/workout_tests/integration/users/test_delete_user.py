from http import HTTPStatus

from workout_management.extensions import db_context
from workout_management.models import User
from workout_tests.bootstrap import BaseTestCase


class UserDeletionTestCase(BaseTestCase):
    def setUp(self, **kwargs):
        super(UserDeletionTestCase, self).setUp()
        self.user = self.create_user()

    def tearDown(self):
        super(UserDeletionTestCase, self).tearDown()

    def test_delete_user(self):
        result = self.client.delete(f"/users/{self._auth_user.id}")

        self.assert200(result)

    def test_delete_differente_user_from_authenticated(self):
        result = self.client.delete(f"/users/{self.user.id}")

        self.assertStatus(result, HTTPStatus.FORBIDDEN)

    def test_create_user_with_inexistent_id(self):
        result = self.client.delete(f"/users/99999")

        self.assert404(result)
