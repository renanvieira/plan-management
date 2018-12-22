import base64
import random
import string
from datetime import datetime

from flask.testing import FlaskClient
from flask_alembic import Alembic
from flask_testing import TestCase

from workout_management.app import create_app
from workout_management.config import ConfigEnum
from workout_management.extensions import db_context
from workout_management.models import User, Plan, Day, Exercise


class TestingClientAdapter:

    def __init__(self, client: FlaskClient, headers=None):
        self.__client = client
        self.__headers = headers

    def post(self, *args, **kwargs):
        kwargs = self.__merge_kwargs(**kwargs)
        return self.__client.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs = self.__merge_kwargs(**kwargs)
        return self.__client.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs = self.__merge_kwargs(**kwargs)
        return self.__client.delete(*args, **kwargs)

    def __merge_kwargs(self, **kwargs):
        if "headers" in kwargs:
            kwargs["headers"] = {**kwargs["headers"], **self.__headers}
        else:
            kwargs["headers"] = self.__headers
        return kwargs


class BaseTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        self._auth_user = None
        self.token_expiration = 300
        super(BaseTestCase, self).__init__(*args, **kwargs)

    def create_user(self, password="123$456#", deleted=False):
        signup_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"user@test{''.join(random.choices(string.ascii_lowercase, k=5))}.com",
            "birth_date": "1990-11-21",
            "password": password
        }

        if deleted:
            signup_data["deleted_at"] = datetime.utcnow()

        user = User(**signup_data)

        db_context.session.add(user)
        db_context.session.commit()

        return user

    def create_plan(self, create_payload, name=None):
        name = name if name is not None else create_payload["name"]
        plan = Plan(name=name)

        for item in create_payload["days"]:
            day = Day.new_from_dict(item)
            plan.days.append(day)

        db_context.session.add(plan)
        db_context.session.commit()
        return plan

    def clean_users(self):
        for user in User.query.all():
            db_context.session.delete(user)
        db_context.session.commit()

    def setUp(self, need_auth=True):
        self.clean_users()
        self.app.config["JWT_EXPIRATION_IN_SECONDS"] = self.token_expiration

        if need_auth:
            self.access_token = self.do_login()
            self.default_headers = dict(Authorization=f"Bearer {self.access_token}")
            self.default_client = self.client
            self.client = TestingClientAdapter(self.client, self.default_headers)

        super(BaseTestCase, self).setUp()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        del self.client

        if self._auth_user is not None:
            self.clean_users()

        for exercise in Exercise.query.all():
            db_context.session.delete(exercise)

        for day in Day.query.all():
            db_context.session.delete(day)

        for plan in Plan.query.all():
            db_context.session.delete(plan)

        for user in User.query.filter(~User.plans.any()).all():
            db_context.session.delete(user)
        db_context.session.commit()

    def create_app(self):
        app = create_app(ConfigEnum.Testing)

        return app

    def do_login(self):
        passwd_plain_text = "123456"
        user = self.create_user(passwd_plain_text)
        self._auth_user = user

        byte_string = f"{user.email}:{passwd_plain_text}".encode("utf-8")
        auth_header = base64.b64encode(byte_string).decode("utf-8")

        result = self.client.post("/auth/login", headers={"Authorization": f"Basic {auth_header}"})

        self.assert200(result)
        return result.json["access_token"]
