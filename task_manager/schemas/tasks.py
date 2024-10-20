from marshmallow import Schema, fields


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    images = fields.List(fields.Nested(
        'ImageSchema',
        )
    )
    faces_counter = fields.Int(missing=0)
    women_counter = fields.Int(missing=0)
    male_counter = fields.Int(missing=0)
    men_avg_age = fields.Float(missing=0.0)
    women_avg_age = fields.Float(missing=0.0)

class TaskResponseSchema(Schema):
    id = fields.Int()
    images = fields.List(fields.Nested('ImageResponseSchema'))
    faces_counter = fields.Int(missing=0)
    women_counter = fields.Int(missing=0)
    male_counter = fields.Int(missing=0)
    men_avg_age = fields.Float(missing=0.0)
    women_avg_age = fields.Float(missing=0.0)
    title = fields.Str()
