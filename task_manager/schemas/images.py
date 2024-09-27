from marshmallow import Schema, fields


class ImageSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str()
    unique_filename = fields.Str()
    filepath = fields.Str()
    task_id = fields.Int()
    faces = fields.List(fields.Nested(
        'FaceSchema',
        exclude=("image_id",))
    )

class ImageResponseSchema(Schema):
    filename = fields.Str()
    faces = fields.List(fields.Nested(
        'FaceSchema',
        exclude=("image_id",))
    )
