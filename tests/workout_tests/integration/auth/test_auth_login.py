import base64
from time import sleep

from workout_tests.bootstrap import BaseTestCase


class AuthLoginTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        self.token_expiration = 2
        super(AuthLoginTestCase, self).setUp(need_auth=False)
        self.user_passwd = "123456$"
        self.user = self.create_user(password=self.user_passwd)

    def test_login(self):
        base64_str = base64.b64encode(f"{self.user.email}:{self.user_passwd}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result = self.client.post("/auth/login", headers={"Authorization": auth_header})

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("access_token", result.json)

    def test_login_with_deleted_user(self):
        deleted_user = self.create_user(password=self.user_passwd, deleted=True)

        base64_str = base64.b64encode(f"{deleted_user.email}:{self.user_passwd}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result = self.client.post("/auth/login", headers={"Authorization": auth_header})

        self.assert401(result)

    def test_login_invalid_password(self):
        base64_str = base64.b64encode(f"{self.user.email}:{'abc123'}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result = self.client.post("/auth/login", headers={"Authorization": auth_header})

        self.assert401(result)

    def test_refresh_token(self):
        base64_str = base64.b64encode(f"{self.user.email}:{self.user_passwd}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result_login = self.client.post("/auth/login", headers={"Authorization": auth_header})
        self.assert200(result_login)
        self.assertIsNotNone(result_login.json)
        self.assertIn("access_token", result_login.json)

        sleep(1)  # Magic sleep number to validate the time after expiration the token can be refreshed
        data = dict(access_token=result_login.json["access_token"])
        result_refresh = self.client.post("/auth/refresh_token", json=data)

        self.assert200(result_refresh)
        self.assertIsNotNone(result_refresh.json)
        self.assertIn("access_token", result_refresh.json)

    def test_refresh_token_after_time(self):
        base64_str = base64.b64encode(f"{self.user.email}:{self.user_passwd}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result_login = self.client.post("/auth/login", headers={"Authorization": auth_header})
        self.assert200(result_login)
        self.assertIsNotNone(result_login.json)
        self.assertIn("access_token", result_login.json)

        sleep(2)  # Magic sleep number to validate the time after expiration the token can be refreshed
        data = dict(access_token=result_login.json["access_token"])
        result_refresh = self.client.post("/auth/refresh_token", json=data)

        self.assert400(result_refresh)

    def test_refresh_token_with_invalid_body(self):
        base64_str = base64.b64encode(f"{self.user.email}:{self.user_passwd}".encode("utf-8"))
        auth_header = f"Basic {base64_str.decode('utf-8')}"

        result_login = self.client.post("/auth/login", headers={"Authorization": auth_header})
        self.assert200(result_login)
        self.assertIsNotNone(result_login.json)
        self.assertIn("access_token", result_login.json)

        data = dict(token=result_login.json["access_token"])
        result_refresh = self.client.post("/auth/refresh_token", json=data)

        self.assert400(result_refresh)

    def test_edit_user_after_token_expires(self):

        user = self.create_user()

        new_data = {
            "first_name": "Testing",
            "last_name": "User Application"
        }
        sleep(1.5)
        result = self.client.post(f"/users/{user.id}", json=new_data)

        self.assert401(result)
