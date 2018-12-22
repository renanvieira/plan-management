import json
from os.path import abspath

from workout_management.extensions import db_context
from workout_management.models import Plan, User, Day, Exercise
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class ExerciseListTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(ExerciseListTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())
            self.plans = list()
            for i in range(1, 4):
                self.plans.append(self.create_plan(self.create_payload))

    def tearDown(self):
        super(ExerciseListTestCase, self).tearDown()

    def test_list_exercises(self):
        result = self.client.get(f"/exercises")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(30, result.json["total"])
