from marshmallow import Schema, fields


class TaskSchemaAdd(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    images = fields.List(fields.Nested(
        'ImageSchemaAdd',
        exclude=("task_id",))
    )
    faces_counter = fields.Int(missing=0)
    women_counter = fields.Int(missing=0)
    male_counter = fields.Int(missing=0)
    men_avg_age = fields.Float(missing=0.0)
    women_avg_age = fields.Float(missing=0.0)

class TaskSchemaResponse(Schema):
    id = fields.Int(dump_only=True)
    images = fields.List(fields.Nested('ImageSchemaResponse'))
    faces_counter = fields.Int(missing=0)
    women_counter = fields.Int(missing=0)
    male_counter = fields.Int(missing=0)
    men_avg_age = fields.Float(missing=0.0)
    women_avg_age = fields.Float(missing=0.0)
