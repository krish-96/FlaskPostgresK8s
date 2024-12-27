from flask_restx import fields

model = {
    "string_field": fields.String(description="A string field"),
    "integer_field": fields.Integer(description="An integer field"),
    "float_field": fields.Float(description="A float field"),
    "boolean_field": fields.Boolean(description="A boolean field"),
    "date_field": fields.Date(description="A date field (YYYY-MM-DD)"),
    "datetime_field": fields.DateTime(description="A datetime field (ISO 8601)"),
    "raw_field": fields.Raw(description="A raw field with no type validation"),
    "list_field": fields.List(fields.String, description="A list of strings"),
    "nested_field": fields.Nested(
        {
            "nested_key1": fields.String(description="Nested key 1"),
            "nested_key2": fields.Integer(description="Nested key 2"),
        },
        description="A nested field"
    ),
    "url_field": fields.Url(description="A URL field"),
    "uuid_field": fields.UUID(description="A UUID field"),
    "dict_field": fields.String(description="A dictionary field (JSON)"),
    "fixed_field": fields.Fixed(precision=2, description="A fixed-precision decimal field"),
    "enum_field": fields.String(
        enum=["Option1", "Option2", "Option3"],
        description="An enumerated string field with limited choices"
    ),
    "binary_field": fields.String(description="Binary data as a base64-encoded string"),
}
