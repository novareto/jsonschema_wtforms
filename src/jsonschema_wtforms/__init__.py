import wtforms.form
from jsonschema_wtforms.field import ObjectParameters
from typing import Dict, Iterable, Optional


JSONSchema = Dict


class Form(wtforms.form.BaseForm):

    def __init__(self, *args, **kwargs):
        self.form_errors = []  # this exists in 3.0a1
        super().__init__(*args, **kwargs)

    @classmethod
    def from_schema(
            cls, schema: JSONSchema,
            include: Optional[Iterable[str]] = None,
            exclude: Optional[Iterable[str]] = None
    ):
        root = ObjectParameters.from_json_field(
            None, False, schema,
            include=include, exclude=exclude)
        return cls(root.fields)
