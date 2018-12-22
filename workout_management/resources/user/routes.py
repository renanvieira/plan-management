import json
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, g
from flask import request

from workout_management.auth import login_required
from workout_management.db import db_context as db
from workout_management.models import User
from workout_management.resources.error import ResponseError, ObjectNotFound, ValidationError, \
    ObjectAlreadyRegisteredError
from workout_management.resources.user.schemas import user_schema, user_edit_schema

user_bluprint = Blueprint("user", __name__)


@user_bluprint.route("/users", methods=["POST"])
def create_user():
    schema, errors = user_schema.load(request.get_json())
    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        if User.query.filter_by(email=schema["email"]).count() > 0:
            return json.dumps(
                ObjectAlreadyRegisteredError().new("email", "email", schema["email"])), HTTPStatus.BAD_REQUEST

        user = User(**schema)

        db.session.add(user)
        db.session.commit()

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR

    return json.dumps(user_schema.dump(user).data)


@user_bluprint.route("/users/<int:id>", methods=["DELETE"])
@login_required
def delete_user(id):
    try:
        user_model = User.query.filter(User.id == id, User.deleted_at.is_(None)).first()

        if user_model is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        if g.logged_user.id != id:
            return json.dumps(
                ResponseError.new_generic_error("You are not authorized to to this operation.")), HTTPStatus.FORBIDDEN

        user_model.deleted_at = datetime.utcnow()

        db.session.add(user_model)
        db.session.commit()

        return json.dumps(user_schema.dump(user_model).data), HTTPStatus.OK

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bluprint.route("/users/<int:id>", methods=["POST"])
@login_required
def edit_user(id):
    try:
        schema, errors = user_edit_schema.load(request.get_json())
        if errors:
            return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

        user = User.query.filter(User.id == id, User.deleted_at.is_(None)).first()

        if user is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        if g.logged_user.id != id:
            return json.dumps(
                ResponseError.new_generic_error("You are not authorized to to this operation.")), HTTPStatus.FORBIDDEN

        for key, val in schema.items():
            if key != "password":
                setattr(user, key, val)
            else:
                user.set_password(val)

        db.session.add(user)
        db.session.commit()

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR

    return json.dumps(user_schema.dump(user).data)
