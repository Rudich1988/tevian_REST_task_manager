from marshmallow import Schema, fields


class FaceSchema(Schema):
    id = fields.Int(dump_only=True)
    bounding_box = fields.Dict()
    gender = fields.Str()
    age = fields.Float()
    image_id = fields.Int()
