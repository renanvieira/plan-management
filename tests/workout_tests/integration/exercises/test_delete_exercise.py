import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from workout_management.extensions import db_context
from workout_management.models import Exercise, Day
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.exercises import __location__


class ExerciseDeleteTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(ExerciseDeleteTestCase, self).setUp()
        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            plan_create_payload = json.loads(payload.read())
            self.plan = self.create_plan(plan_create_payload)

        self.exercise = Exercise(name="Romanian Deadlift", sets=3, reps=12)
        self.exercise.day = Day(number=1, plan=self.plan)
        db_context.session.add(self.exercise)
        db_context.session.commit()

    def tearDown(self):
        super(ExerciseDeleteTestCase, self).tearDown()

    def test_delete_exercise(self):
        result = self.client.delete(f"/exercises/{self.exercise.id}")

        self.assert200(result)

    def test_delete_exercise_invalid_id(self):
        result = self.client.delete(f"/exercises/9999996")

        self.assert404(result)

    @mock.patch.object(Exercise, "query", new_callable=PropertyMock)
    def test_delete_exercise_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = self.raise_exception

        data = {
            "name": "Inclined Bench Press",
            "sets": 3,
            "reps": 12,
            "plan": self.plan.id,
            "day_number": 4
        }

        result = self.client.delete(f"/exercises/{self.exercise.id}", json=data)

        self.assert500(result)
