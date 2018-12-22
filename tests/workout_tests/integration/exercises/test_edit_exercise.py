import json
from os.path import abspath

from workout_management.extensions import db_context
from workout_management.models import User, Plan, Exercise, Day
from workout_tests.bootstrap import BaseTestCase
from workout_tests.integration.exercises import __location__


class ExerciseEditTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(ExerciseEditTestCase, self).setUp()
        with open(abspath(__location__ + "/raw_requests/plan_full_payload.json")) as payload:
            plan_create_payload = json.loads(payload.read())
            self.plan = self.create_plan(plan_create_payload)

        self.exercise = Exercise(name="Romanian Deadlift", sets=3, reps=12)
        self.exercise.day = Day(number=1, plan=self.plan)
        db_context.session.add(self.exercise)
        db_context.session.commit()

    def tearDown(self):
        super(ExerciseEditTestCase, self).tearDown()

    def test_edit_exercise(self):

        new_data = {
            "name": "Sumo Deadlift",
            "reps": 20
        }

        result = self.client.post(f"/exercises/{self.exercise.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["name"], "Sumo Deadlift")
        self.assertEqual(result.json["reps"], 20)

    def test_edit_exercise_invalid_body(self):

        new_data = {
            "reps": "ABC"
        }

        result = self.client.post(f"/exercises/{self.exercise.id}", json=new_data)

        self.assert400(result)

    def test_edit_exercise_invalid_id(self):

        new_data = {
            "name": "Sumo Deadlift"
        }

        result = self.client.post(f"/exercises/9999996", json=new_data)

        self.assert404(result)
