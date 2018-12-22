from marshmallow import Schema
from marshmallow.fields import String, Date, Email, DateTime, Integer
from marshmallow.validate import Length


class UserSchema(Schema):
    id = Integer(dump_only=True)
    first_name = String(required=True, validate=Length(1, 64))
    last_name = String(required=True, validate=Length(1, 64))
    birth_date = Date(required=True)
    email = Email(required=True)
    password = String(required=True, validate=Length(5, 32), load_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)
    deleted_at = DateTime(dump_only=True)


class UserEditSchema(Schema):
    id = Integer(dump_only=True)
    first_name = String(required=False, validate=Length(1, 64))
    last_name = String(required=False, validate=Length(1, 64))
    birth_date = Date(required=False)
    email = Email(required=False)
    password = String(required=False, validate=Length(5, 32), load_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)
    deleted_at = DateTime(dump_only=True)


user_schema = UserSchema()
user_edit_schema = UserEditSchema()
