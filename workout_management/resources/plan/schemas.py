from marshmallow import Schema
from marshmallow.fields import Integer, String, DateTime, Nested, Boolean
from marshmallow.validate import Length

from workout_management.resources.exercises.schemas import ExerciseSchema


class PlanSchema(Schema):
    id = Integer(dump_only=True)
    name = String(validate=Length(1, 64), required=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)
    deleted_at = DateTime(dump_only=True)


class AssociatedSchema(Schema):
    id = Integer(dump_only=True)
    user = Integer(load_only=True, required=True)
    associated_user_count = Integer()


class DaySchema(Schema):
    number = Integer()
    exercises = Nested(ExerciseSchema, required=True, many=True)


class DayListSchema(Schema):
    limit = Integer(default=10)
    total = Integer()
    total_pages = Integer(load_from="pages")
    items = Nested(DaySchema, many=True)
    has_more = Boolean(load_from="has_next")


class PlanFullSchema(PlanSchema):
    days = Nested(DaySchema, many=True)


class PlanListSchema(Schema):
    limit = Integer(default=10)
    total = Integer()
    total_pages = Integer(load_from="pages")
    items = Nested(PlanSchema, many=True)
    has_more = Boolean(load_from="has_next")


day_schema = DaySchema()
plan_schema = PlanSchema()
plan_full_schema = PlanFullSchema()
plan_list_schema = PlanListSchema()
assciation_user_plan_schema = AssociatedSchema()
day_list_schema = DayListSchema()
