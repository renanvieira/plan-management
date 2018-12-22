import json
from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

import jwt
from flask import current_app as app, request, g
from jwt import ExpiredSignatureError

from workout_management.models import User


def parse_bearer_token(request):
    if "Authorization" not in request.headers:
        raise ValueError("header Authorization not found")

    header = request.headers.get("Authorization")
    splitted = header.split(' ')
    return splitted[0], splitted[1]


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            token_type, access_token = parse_bearer_token(request)
        except ValueError as val_err:
            return json.dumps(dict(error={"message": "You need to be authenticated."})), HTTPStatus.UNAUTHORIZED

        result, opened_token = verify_token(access_token)

        if result is True:

            user = User.query.filter(User.id == opened_token["sub"], User.deleted_at.is_(None)).first()

            if user is not None:
                g.access_token = access_token
                g.jwt = opened_token
                g.logged_user = user
        else:
            return json.dumps(dict(error={
                "message": "You are not authorized. Please sign in and use the new access_token."})), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return wrap


def verify_token(token, **kwargs):
    try:
        result = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'], **kwargs)
        return True, result
    except ExpiredSignatureError as sig_error:
        return False, None


def refresh_token(access_token):
    validation_result, open_token = verify_token(access_token, verify=False)

    current_exp_date = datetime.utcfromtimestamp(open_token["exp"])
    current_utc_date = datetime.utcnow()
    diff_in_seconds = (current_exp_date - current_utc_date).total_seconds()

    if 0 < diff_in_seconds <= app.config["JWT_EXPIRATION_IN_SECONDS"]:
        new_expiration = datetime.utcnow() + timedelta(seconds=app.config["JWT_EXPIRATION_IN_SECONDS"])
        open_token["exp"] = new_expiration
        return jwt.encode(open_token, app.config["SECRET_KEY"])
    else:
        raise ExpiredSignatureError("Token too old to be refreshed")


def generate_token(user: User):
    expiration = datetime.utcnow() + timedelta(seconds=app.config["JWT_EXPIRATION_IN_SECONDS"])
    issued_at = datetime.utcnow()
    token_data = dict(name=user.full_name, sub=user.id, exp=expiration, iat=issued_at)

    return jwt.encode(token_data, app.config["SECRET_KEY"])


def authenticate_basic_auth(authorization):
    return authenticate(authorization.username, authorization.password)


def authenticate(username, password):
    user = User.query.filter(User.email == username, User.deleted_at.is_(None)).first()
    if user and user.check_password(password):
        return user
