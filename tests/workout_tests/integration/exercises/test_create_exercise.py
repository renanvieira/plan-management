import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_tests.bootstrap import BaseTestCase, Plan
from workout_tests.integration.exercises import __location__


class ExerciseCreationTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(ExerciseCreationTestCase, self).setUp()
        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.plan_create_payload = json.loads(payload.read())
            self.plan = self.create_plan(self.plan_create_payload)

    def tearDown(self):
        super(ExerciseCreationTestCase, self).tearDown()

    def test_create_exercise(self):
        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 3
        }

        result = self.client.post("/exercises", json=data)

        self.assert200(result)

    def test_create_exercise_with_invalid_body(self):
        data = {
            "name": "Inclined Bench Press",
            "sets": "abc",
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 3
        }

        result = self.client.post("/exercises", json=data)

        self.assert400(result)

    def test_create_exercise_with_inexistent_day(self):
        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 4
        }

        result = self.client.post("/exercises", json=data)

        self.assert200(result)

    def test_create_exercise_with_invalid_plan(self):
        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": 999999998,
            "day_number": 4
        }

        result = self.client.post("/exercises", json=data)

        self.assert400(result)

    def test_create_exercise_without_authentication(self):
        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 4
        }

        result2 = self.default_client.post("/exercises", json=data)

        self.assert401(result2)

    @mock.patch.object(Plan, "query", new_callable=PropertyMock)
    def test_create_exercise_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = self.raise_exception

        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 4
        }

        result = self.client.post(f"/exercises", json=data)

        self.assert500(result)
