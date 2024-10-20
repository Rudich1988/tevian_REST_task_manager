from marshmallow import Schema, fields, post_load


class ImageResponseSchema(Schema):
    id = fields.Int()
    filename = fields.Str()
    unique_filename = fields.Str()
    filepath = fields.Str()
    task_id = fields.Int()
    faces = fields.List(fields.Nested(
        'FaceSchema',
        exclude=("image_id",))
    )

class ImageSchema(Schema):
    filename = fields.Str()
    faces = fields.List(fields.Nested(
        'FaceSchema',
        exclude=("image_id",))
    )
    id = fields.Int(load_only=True)
    unique_filename = fields.Str(load_only=True)
    filepath = fields.Str(load_only=True)
    task_id = fields.Int(load_only=True)

    @post_load
    def remove_fields(self, data, **kwargs):
        data.pop('task_id', None)
        data.pop('unique_filename', None)
        data.pop('filepath', None)
        data.pop('id', None)
        return data
