from marshmallow import Schema, fields, validate

class ColaboradorSchema(Schema):
    nome = fields.String(required=True)
    email = fields.Email(required=True)
    senha = fields.String(required=True, validate=validate.Length(min=6))
    cargo = fields.String(required=True)
    salario = fields.Float(required=True)
