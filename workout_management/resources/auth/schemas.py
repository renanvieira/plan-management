from marshmallow import Schema
from marshmallow.fields import String


class RefreshTokenSchema(Schema):
    access_token = String(required=True)


refresh_token_schema = RefreshTokenSchema()
