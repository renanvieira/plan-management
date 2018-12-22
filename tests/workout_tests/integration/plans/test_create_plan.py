import json
from os.path import abspath

from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class PlanCreationTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(PlanCreationTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())

        with open(abspath(__location__ + "/raw_requests/plan_full_payload_without_name.json")) as payload:
            self.create_payload_without_name = json.loads(payload.read())

    def tearDown(self):
        super(PlanCreationTestCase, self).tearDown()

    def test_create_plan(self):
        result = self.client.post("/plans", json=self.create_payload)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))

    def test_create_plan_without_name(self):
        result = self.client.post("/plans", json=self.create_payload_without_name)

        self.assert400(result)

    def test_create_plans_with_same_email(self):
        plan = self.create_plan(self.create_payload)

        result2 = self.client.post("/plans", json=self.create_payload)

        self.assertIsNotNone(plan)
        self.assert400(result2)

    def test_create_plans_without_authentication(self):
        result2 = self.default_client.post("/plans", json=self.create_payload)

        self.assert401(result2)
