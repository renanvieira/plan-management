from http import HTTPStatus
from unittest import mock
from unittest.mock import PropertyMock, Mock

from workout_tests.bootstrap import BaseTestCase, User


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

    @mock.patch.object(User, "query", new_callable=PropertyMock)
    def test_delete_user_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = [Mock(autospec=True), self.raise_exception]

        result = self.client.delete(f"/users/{self._auth_user.id}")

        self.assert500(result)
