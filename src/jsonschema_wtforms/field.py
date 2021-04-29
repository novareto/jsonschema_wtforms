from typing import Optional, Iterable, Any, TypedDict
from jsonschema_wtforms._fields import MultiCheckboxField
from jsonschema_wtforms.validators import NumberRange


Choices = Optional[List[Any]]


converters = {
    "string": wtforms.fields.StringField,
    "integer": wtforms.fields.IntegerField,
    "number": wtforms.fields.FloatField,
    "boolean": wtforms.fields.BooleanField,
    "array": MultiCheckboxField,
    "$ref": wtforms.fields.FormField
}


def constraints_from_params(type_: str, required: bool, **params):
    constraints = {
        'validators': []
    }
    if required:
        constraints['validators'].append(wtforms.validators.DataRequired())
    else:
        constraints['validators'].append(wtforms.validators.Optional())
    if 'min' in params or 'max' in params:
        constraints['validators'].append(NumberRange(
            min=params.pop('minimum', None),
            max=params.pop('maximum', None),
            exclusive_min=params.pop('exclusiveMinimum', False),
            exclusive_max=params.pop('exclusiveMaximum', False)
        ))
    if (enum := params.pop('enum', None)) is not None:
        constraints['choices'] = enum
    if (min_entries := params.pop('minItems', None)) is not None:
        constraints['min_entries'] = min_entries
    if (max_entries := params.pop('maxItems', None)) is not None:
        constraints['max_entries'] = max_entries
    if params:
        raise NotImplementedError(
            f'Field parameters were not all consumed: {params}')

    return constraints


class Metadata(TypedDict):
    default: Any
    description: str
    label: str


class Field:
    type_: string
    metadata: Metadata
    required: bool
    readonly: bool = False
    choices: Choices = None
    factory: Optional[wtforms.fields.Field] = None
    subfield: wtforms.fields.Field = None

    def __init__(self, name, required, **params):
        self.required = required
        self.type_ = params.pop('type', None)
        if not isinstance(self.type_, str):
            raise NotImplementedError(
                f"Property {name}: unsupported type '{self.type_!r}'.")
        self.required = required
        self.metadata = {
            'default': params.pop('default', None),
            'description': params.pop('descriptions', None),
            'label': params.pop('title', name),
        }
        if (items := params.pop('items')) is not None:
            self.subfield = Field(name, required=True, **items)
        self.params = params

    def __call__(self):
        options = constraints_from_params(
            self.type_, self.required, **self.params)

        factory = self.factory  # handpicked factory
        if self.type_ == 'array' and self.subfield is not None:
            if factory is not None:
                assert issubclass(self.factory, wtforms.fields.FieldList)
            else:
                factory = wtforms.fields.FieldList
            return factory(self.subfield(), **{**self.metadata, **options})

        if factory is None:
            factory = converters.get(self.type_)
            if factory is None:
                raise TypeError(
                    f'{self.type_} cannot be converted to a WTForms field'
                )

        return factory(**{**self.metadata, **options})
