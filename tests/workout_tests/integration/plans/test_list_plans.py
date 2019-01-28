import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_management.models import Plan
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class PlanListTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(PlanListTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plans = list()

            for i in range(1, 4):
                self.plans.append(self.create_plan(self.create_payload, f"Test Plan {i}"))

    def tearDown(self):
        super(PlanListTestCase, self).tearDown()

    def test_list_plan(self):
        result = self.client.get(f"/plans")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["total"], 3)

    @mock.patch.object(Plan, "query", new_callable=PropertyMock)
    def test_list_plan_with_error(self, mock_obj):
        mock_obj.return_value.paginate.side_effect = self.raise_exception

        result = self.client.get(f"/plans")

        self.assert500(result)
