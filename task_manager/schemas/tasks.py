from marshmallow import Schema, fields


class TaskSchemaAdd(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    images = fields.List(fields.Nested(
        'ImageSchemaAdd',
        exclude=("task_id",))
    )
