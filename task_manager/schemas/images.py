from marshmallow import Schema, fields


class ImageSchemaAdd(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str()
    task_id = fields.Int()
    faces = fields.List(fields.Nested('FaceSchema',
                                      exclude=("image_id",)))
