import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_tests.bootstrap import BaseTestCase, Day
from workout_tests.integration.plans import __location__


class PlanDaysTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(PlanDaysTestCase, self).setUp()
        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plan = self.create_plan(self.create_payload)

    def tearDown(self):
        super(PlanDaysTestCase, self).tearDown()

    def test_add_work_days(self):
        new_day = self.create_payload["days"][-1]
        new_day["number"] += 1

        result = self.client.post(f"/plans/{self.plan.id}/days", json=new_day)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("number", result.json)
        self.assertIn("exercises", result.json)
        self.assertEqual(len(result.json["exercises"]), len(new_day["exercises"]))

        self.create_payload["days"].append(new_day)

    def test_add_work_days_with_invalid_plan_id(self):
        new_day = self.create_payload["days"][-1]
        new_day["number"] += 1

        result = self.client.post(f"/plans/{9999996}/days", json=new_day)

        self.assert404(result)

    def test_delete_workout_days(self):
        new_day = self.create_payload["days"][-1]

        result = self.client.delete(f"/plans/{self.plan.id}/days/{new_day['number']}")

        self.assert200(result)

    def test_delete_workout_days_with_invalid_plan_id(self):
        new_day = self.create_payload["days"][-1]

        result = self.client.delete(f"/plans/{9999999996}/days/{new_day['number']}")

        self.assert404(result)

    def test_delete_workout_days_with_invalid_day_number(self):
        result = self.client.delete(f"/plans/{self.plan.id}/days/{999999225}")

        self.assert404(result)

    def test_get_workout_days(self):
        result = self.client.get(f"/plans/{self.plan.id}/days")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["total"], 3)

    def test_get_workout_days_invalid_plan_id(self):
        result = self.client.get(f"/plans/9999995/days")

        self.assert404(result)

    @mock.patch.object(Day, "query", new_callable=PropertyMock)
    def test_get_plan_days_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        result = self.client.get(f"/plans/{self.plan.id}/days")

        self.assert500(result)
