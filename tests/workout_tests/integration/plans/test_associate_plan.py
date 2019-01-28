import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_tests.bootstrap import BaseTestCase, Plan
from workout_tests.integration.plans import __location__


class AssociateUserToPlanTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(AssociateUserToPlanTestCase, self).setUp()
        self.user = self.create_user()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plan = self.create_plan(self.create_payload)

    def tearDown(self):
        super(AssociateUserToPlanTestCase, self).tearDown()

    def test_associate_plan(self):
        new_data = {
            "user": self._auth_user.id
        }

        result = self.client.post(f"/plans/{self.plan.id}/enroll", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertIn("associated_user_count", result.json)

    def test_associate_plan_to_user_multiple_times(self):
        new_data = {
            "user": self._auth_user.id
        }

        result = self.client.post(f"/plans/{self.plan.id}/enroll", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertIn("associated_user_count", result.json)

        result2 = self.client.post(f"/plans/{self.plan.id}/enroll", json=new_data)
        self.assert400(result2)

    def test_associate_plan_with_invalid_plan_id(self):
        new_data = {
            "user": self.user.id
        }

        result = self.client.post(f"/plans/{9999996}/enroll", json=new_data)

        self.assert404(result)

    def test_associate_plan_with_invalid_user_id(self):
        new_data = {
            "user": 9999966
        }

        result = self.client.post(f"/plans/{self.plan.id}/enroll", json=new_data)

        self.assert404(result)

    def test_associate_plan_with_invalid_body_param(self):
        new_data = {
            "user": "abc"
        }

        result = self.client.post(f"/plans/{self.plan.id}/enroll", json=new_data)

        self.assert400(result)

    @mock.patch.object(Plan, "query", new_callable=PropertyMock)
    def test_associate_plan_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        new_data = {
            "name": "Summer Plan"
        }

        result = self.client.post(f"/plans/{self.plan.id}", json=new_data)

        self.assert500(result)
