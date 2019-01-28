import json
from _datetime import datetime
from http import HTTPStatus

from flask import Blueprint
from flask import request, current_app as app

from workout_management.auth import login_required
from workout_management.db import db_context as db
from workout_management.helpers import PaginatorHelper
from workout_management.models import (Plan, User, Day, Exercise)
from workout_management.resources.error import (ResponseError,
                                                ValidationError,
                                                ObjectAlreadyRegisteredError,
                                                ObjectNotFound,
                                                PlanAlreadyAssociatedError)
from workout_management.resources.plan.schemas import (plan_schema,
                                                       assciation_user_plan_schema,
                                                       day_schema,
                                                       plan_full_schema,
                                                       plan_list_schema, day_list_schema)

plan_blueprint = Blueprint("plan", __name__)


@plan_blueprint.route("/plans", methods=["POST"])
@login_required
def create_plan():
    schema, errors = plan_full_schema.load(request.get_json())

    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        if Plan.query.filter_by(name=schema["name"]).count() > 0:
            return json.dumps(
                ObjectAlreadyRegisteredError().new("plan", "name", schema["name"])), HTTPStatus.BAD_REQUEST

        plan = Plan(name=schema["name"])

        for item in schema["days"]:
            day = Day.new_from_dict(item)
            plan.days.append(day)

        db.session.add(plan)
        db.session.commit()

    except Exception as e:
        app.logger.exception(e)
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR

    return json.dumps(plan_full_schema.dump(plan).data)


@plan_blueprint.route("/plans/<int:plan_id>", methods=["GET"])
@login_required
def get_plan(plan_id):
    try:

        plan = Plan.query.filter_by(id=plan_id).first()

        if plan is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        return json.dumps(plan_full_schema.dump(plan).data)

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans/<int:id>", methods=["POST"])
@login_required
def edit_plan(id):
    schema, errors = plan_schema.load(request.get_json())
    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        plan = Plan.query.filter_by(id=id).first()

        if plan is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        if Plan.query.filter_by(name=schema["name"]).count() > 0:
            return json.dumps(
                ObjectAlreadyRegisteredError().new("plan", "name", schema["name"])), HTTPStatus.BAD_REQUEST

        for key, val in schema.items():
            setattr(plan, key, val)

        db.session.add(plan)
        db.session.commit()

        plan.notify_users()

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR

    return json.dumps(plan_schema.dump(plan).data)


@plan_blueprint.route("/plans/<int:id>", methods=["DELETE"])
@login_required
def delete_plan(id):
    try:
        plan = Plan.query.filter(Plan.id == id, Plan.deleted_at.is_(None)).first()

        if plan is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        plan.deleted_at = datetime.utcnow()

        db.session.add(plan)
        db.session.commit()

        return plan_full_schema.dumps(plan).data, HTTPStatus.OK

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans/<int:plan_id>/enroll", methods=["POST"])
@login_required
def associate_user_to_plan(plan_id):
    schema, errors = assciation_user_plan_schema.load(request.get_json())
    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        user_id = schema["user"]
        plan = Plan.query.filter_by(id=plan_id).first()
        if plan is None:
            return json.dumps(ObjectNotFound().new_detailed("plan", "id", plan_id)), HTTPStatus.NOT_FOUND

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return json.dumps(ObjectNotFound().new_detailed("user", "id", user_id)), HTTPStatus.NOT_FOUND

        if user in plan.users:
            return json.dumps(PlanAlreadyAssociatedError.new("user", "user_id", user_id)), HTTPStatus.BAD_REQUEST

        plan.users.append(user)

        db.session.add(plan)
        db.session.commit()
        plan.notify_association(user)

        return json.dumps(assciation_user_plan_schema.dump(plan).data)

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans", methods=["GET"])
@login_required
def list_all_plans():
    try:
        page = int(request.args.get("page", 1))

        plan_paginator = Plan.query.paginate(page, 2)

        paginated_data = PaginatorHelper.get_paginator_dict(plan_paginator)

        return plan_list_schema.dumps(paginated_data).data

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans/<int:plan_id>/days", methods=["POST"])
@login_required
def add_workout_day(plan_id):
    schema, errors = day_schema.load(request.get_json())
    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        plan = Plan.query.filter_by(id=plan_id).first()

        if plan is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        day_number = int(schema["number"])

        if Plan.query.filter(Plan.days.any(number=day_number)).count() > 0:
            return json.dumps(
                ObjectAlreadyRegisteredError().new("day", "number", schema["number"])), HTTPStatus.BAD_REQUEST

        schema["exercises"] = list({val["name"].strip().title(): val for val in schema["exercises"]}.values())

        exercises = [Exercise(**item) for item in schema["exercises"]]

        day = Day(number=schema["number"], plan=plan, exercises=exercises)

        db.session.add(day)
        db.session.commit()

        plan.notify_users()

        return json.dumps(day_schema.dump(day).data)
    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans/<int:plan_id>/days", methods=["GET"])
@login_required
def get_workout_days(plan_id):
    try:

        page = int(request.args.get("page", 1))

        query = Day.query.filter_by(plan_id=plan_id)

        days_paginator = query.paginate(page, int(app.config["ITEMS_PER_PAGE"]))

        if days_paginator is None or query.count() == 0:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        paginated_data = PaginatorHelper.get_paginator_dict(days_paginator)

        return day_list_schema.dumps(paginated_data).data

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@plan_blueprint.route("/plans/<int:plan_id>/days/<int:day_number>", methods=["DELETE"])
@login_required
def delete_workout_day(plan_id, day_number):
    day = Day.query.filter(Day.plan_id == plan_id, Day.number == day_number).first()

    if day is None:
        return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

    for exercise in day.exercises:
        db.session.delete(exercise)

    db.session.delete(day)
    db.session.commit()

    return json.dumps({}), HTTPStatus.OK
