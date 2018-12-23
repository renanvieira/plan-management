import json
from os.path import abspath

from workout_management.extensions import db_context
from workout_management.models import Day, Exercise
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.plans import __location__


class ExerciseListTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(ExerciseListTestCase, self).setUp()

        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            self.create_payload = json.loads(payload.read())

        self.plan = self.create_plan(self.create_payload)
        self.exercise = Exercise(name="Romanian Deadlift", sets=3, reps=12)
        self.exercise.day = Day(number=1, plan=self.plan)

        db_context.session.add(self.exercise)
        db_context.session.commit()

    def tearDown(self):
        super(ExerciseListTestCase, self).tearDown()

    def test_get_exercises(self):
        result = self.client.get(f"/exercises/{self.exercise.id}")

        self.assert200(result)
        self.assertIsNotNone(result.json)


    def test_get_exercises_with_invalid_id(self):
        result = self.client.get(f"/exercises/9999994")

        self.assert404(result)