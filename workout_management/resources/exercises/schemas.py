from marshmallow import Schema
from marshmallow.fields import Integer, String, DateTime, Nested, Boolean


class ExerciseSchema(Schema):
    id = Integer(dump_only=True)
    name = String(required=True)
    sets = Integer(required=True)
    reps = Integer(required=True)
    plan = Integer(required=False)
    day_number = Integer(required=False)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)
    deleted_at = DateTime(dump_only=True)


class ExerciseEditSchema(Schema):
    id = Integer(dump_only=True)
    name = String(required=False)
    sets = Integer(required=False)
    reps = Integer(required=False)


class ExerciseListSchema(Schema):
    limit = Integer(default=10)
    total = Integer()
    total_pages = Integer(load_from="pages")
    items = Nested(ExerciseSchema, many=True)
    has_more = Boolean(load_from="has_next")


exercise_schema = ExerciseSchema()
exercise_edit_schema = ExerciseEditSchema()
exercise_list_schema = ExerciseListSchema()
