import jsonschema
import wtforms.form
from typing import Dict, Type, Iterable, Optional
from jsonschema_wtforms.field import Field


JSONSchema = Dict


def schema_fields(model, include=None, exclude=None) -> dict:
    if not include:
        include = frozenset(model.__fields__.keys())
    if not exclude:
        exclude = set()

    return {
        name: Field(field) for name, field in model.__fields__.items()
        if name in include and name not in exclude
    }


class Form(wtforms.form.BaseForm):
    schema: Optional[JSONSchema] = None

    def __init__(self, *args, **kwargs):
        self.form_errors = []  # this exists in 3.0a1
        super().__init__(*args, **kwargs)

    @classmethod
    def from_fields(cls, fields: Iterable[Field]):
        fields = {name: field() for name, field in fields.items()}
        return cls(fields)

    @classmethod
    def from_schema(cls, schema: JSONSchema, **kwargs):
        form = cls.from_fields(model_fields(model, **kwargs))
        form.model = model
        return form
