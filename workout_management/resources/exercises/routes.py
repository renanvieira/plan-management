import json
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, request

from workout_management.auth import login_required
from workout_management.db import db_context as db
from workout_management.helpers import PaginatorHelper
from workout_management.models import Exercise, Plan, Day
from workout_management.resources.error import ValidationError, ResponseError, ObjectNotFound
from workout_management.resources.exercises.schemas import exercise_schema, exercise_edit_schema, exercise_list_schema

exercise_blueprint = Blueprint("exercises", __name__)


@exercise_blueprint.route("/exercises", methods=["POST"])
@login_required
def create_exercise():
    schema, errors = exercise_schema.load(request.get_json())

    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        exercise = Exercise(name=schema["name"], sets=schema["sets"], reps=schema["reps"])

        plan = Plan.query.filter(Plan.id == schema["plan"], Plan.deleted_at.is_(None)).first()

        if plan is None:
            return json.dumps(ObjectNotFound.new_detailed("plan", "plan", schema["plan"])), HTTPStatus.BAD_REQUEST

        workout_day_list = list(filter(lambda x: x.number == schema["day_number"], plan.days))

        if len(plan.days) > 0 and len(workout_day_list) > 0:
            workout_day = workout_day_list[0]
        else:
            workout_day = Day(number=1, plan=plan)

        exercise.day = workout_day
        exercise.plan = plan

        db.session.add(exercise)
        db.session.commit()

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR

    return json.dumps(exercise_schema.dump(exercise).data)


@exercise_blueprint.route("/exercises/<int:id>", methods=["POST"])
def edit_exercise(id):
    schema, errors = exercise_edit_schema.load(request.get_json())
    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        for key, val in schema.items():
            setattr(exercise, key, val)

        exercise_schema.updated_at = datetime.utcnow()

        db.session.add(exercise)
        db.session.commit()

        return exercise_schema.dumps(exercise).data

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@exercise_blueprint.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    try:
        exercise = Exercise.query.filter(Exercise.id == id).first()

        if exercise is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        exercise.deleted_at = datetime.utcnow()

        db.session.delete(exercise)
        db.session.commit()

        return json.dumps({}), HTTPStatus.OK

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@exercise_blueprint.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    try:
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        return exercise_schema.dumps(exercise).data

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@exercise_blueprint.route("/exercises", methods=["GET"])
def list_exercises():
    try:
        page = int(request.args.get("page", 1))

        exercise_paginator = Exercise.query.paginate(page, 1)

        paginated_data = PaginatorHelper.get_paginator_dict(exercise_paginator)

        return exercise_list_schema.dumps(paginated_data).data

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR
