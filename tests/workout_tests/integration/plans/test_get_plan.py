import json
from http import HTTPStatus
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_management.models import Plan
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class GetPlanTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(GetPlanTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plan = self.create_plan(self.create_payload)

    def tearDown(self):
        super(GetPlanTestCase, self).tearDown()

    def test_get_plan(self):
        result = self.client.get(f"/plans/{self.plan.id}")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertTrue("id" in result.json)
        self.assertIsNotNone(result.json["id"])
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertIn("created_at", result.json)
        self.assertIn("updated_at", result.json)
        self.assertIn("deleted_at", result.json)

    def test_get_plan_with_invalid_id(self):
        result = self.client.get(f"/plans/{99999}")

        assert result.status_code == HTTPStatus.NOT_FOUND

    @mock.patch.object(Plan, "query", new_callable=PropertyMock)
    def test_get_plan_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        result = self.client.get(f"/plans/{self.plan.id}")

        self.assert500(result)
