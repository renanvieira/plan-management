import json
from os.path import abspath
from unittest.mock import MagicMock

from workout_management.extensions import db_context
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class PlanEditTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(PlanEditTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plan = self.create_plan(self.create_payload)

    def tearDown(self):
        super(PlanEditTestCase, self).tearDown()

    def test_edit_plan(self):
        new_data = {
            "name": "Summer Plan"
        }

        result = self.client.post(f"/plans/{self.plan.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertEqual(result.json["name"], new_data["name"])

    def test_edit_plan_with_user_notification(self):

        self.plan.users.append(self._auth_user)
        db_context.session.add(self.plan)
        db_context.session.commit()

        new_data = {
            "name": "Summer Plan"
        }

        result = self.client.post(f"/plans/{self.plan.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertEqual(result.json["name"], new_data["name"])

    def test_edit_plan_with_long_name(self):
        new_data = {
            "name": "Boca-newlywed-shutout-playbill-surprise-onetime-goddess-tincture-bacon-couplet-Glisten-haul-lazar-undies-campfire-reproof-sensor-upraise-sealskin-pulp"
        }

        result = self.client.post(f"/plans/{self.plan.id}", json=new_data)

        self.assert400(result)

    def test_edit_plan_with_invalid_id(self):
        result = self.client.post(f"/plans/{99999}", json=self.create_payload)

        self.assert404(result)

    def test_edit_plan_with_same_name(self):
        new_data = {
            "name": "Summer Workout Plan"
        }

        result = self.client.post(f"/plans/{self.plan.id}", json=new_data)

        self.assert400(result)
