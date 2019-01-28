import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_tests.bootstrap import BaseTestCase, Plan
from workout_tests.integration.plans import __location__


class PlanDeletionTestCase(BaseTestCase):
    def setUp(self, **kwargs):
        super(PlanDeletionTestCase, self).setUp()
        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            create_payload = json.loads(payload.read())
            self.plan = self.create_plan(create_payload)

    def tearDown(self):
        super(PlanDeletionTestCase, self).tearDown()

    def test_delete_plan(self):
        result = self.client.delete(f"/plans/{self.plan.id}")

        self.assert200(result)

    def test_delete_plan_with_inexistent_id(self):
        result = self.client.delete(f"/plans/999788999")

        self.assert404(result)

    @mock.patch.object(Plan, "query", new_callable=PropertyMock)
    def test_delete_plan_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        result = self.client.delete(f"/plans/{self.plan.id}")

        self.assert500(result)
