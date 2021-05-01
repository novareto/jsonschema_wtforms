import wtforms.form
from jsonschema_wtforms.field import ObjectParameters
from typing import Dict, Iterable, Optional


JSONSchema = Dict


def schema_fields(schema: JSONSchema,
                  include: Optional[Iterable[str]] = None,
                  exclude: Optional[Iterable[str]] = None) -> dict:
    root = ObjectParameters.from_json_field(None, False, schema)
    if not include:
        include = frozenset(root.fields.keys())
    if not exclude:
        exclude = set()
    return {
        name: field for name, field in root.fields.items()
        if name in include and name not in exclude
    }


class Form(wtforms.form.BaseForm):

    def __init__(self, *args, **kwargs):
        self.form_errors = []  # this exists in 3.0a1
        super().__init__(*args, **kwargs)

    @classmethod
    def from_schema(cls, schema: JSONSchema, **kwargs):
        fields = schema_fields(schema, **kwargs)
        return cls(fields)
