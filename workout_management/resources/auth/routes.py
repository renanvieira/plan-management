import json
from http import HTTPStatus

from flask import Blueprint, request
from jwt import ExpiredSignatureError

from workout_management.auth import generate_token, authenticate_basic_auth, refresh_token
from workout_management.resources.auth.schemas import refresh_token_schema
from workout_management.resources.error import ValidationError, JWTExpiredToken

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth/login", methods=["POST"])
def login():
    if request.authorization is None:
        return json.dumps({}), HTTPStatus.BAD_REQUEST

    user = authenticate_basic_auth(request.authorization)

    if user:
        access_token = generate_token(user)
        response_data = {"access_token": access_token.decode("utf-8")}
        return json.dumps(response_data), HTTPStatus.OK
    else:
        return json.dumps({}), HTTPStatus.UNAUTHORIZED


@auth_blueprint.route("/auth/refresh_token", methods=["POST"])
def refresh():
    schema, errors = refresh_token_schema.load(request.get_json())

    if errors:
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(errors)), HTTPStatus.BAD_REQUEST

    try:
        access_token = refresh_token(schema["access_token"])
        response_data = {"access_token": access_token.decode("utf-8")}

        return json.dumps(response_data), HTTPStatus.OK

    except ExpiredSignatureError as exp_error:
        return json.dumps(JWTExpiredToken.new_generic_error(JWTExpiredToken.MESSAGE)), HTTPStatus.BAD_REQUEST
