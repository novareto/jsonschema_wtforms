import wtforms.fields
from typing import Optional, List, Any, TypedDict
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


def constraints_from_params(required: bool = False, **params):
    """Extract constraints from parameters.
    This is agnostic, it won't check if the constraints match the type.
    This kind of verification belongs to the schema.
    """
    constraints = {
        'validators': []
    }
    available = set(params.keys())
    if required:
        constraints['validators'].append(wtforms.validators.DataRequired())
    else:
        constraints['validators'].append(wtforms.validators.Optional())
    if {'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'
       } & available:
        constraints['validators'].append(NumberRange(
            min=params.pop('minimum', None),
            max=params.pop('maximum', None),
            exclusive_min=params.pop('exclusiveMinimum', None),
            exclusive_max=params.pop('exclusiveMaximum', None)
        ))
    if {'minLength', 'maxLength'} & available:
        constraints['validators'].append(wtforms.validators.Length(
            min=params.pop('minLength', -1),
            max=params.pop('maxLength', -1)
        ))
    if 'pattern' in params:
        constraints['validators'].append(wtforms.validators.Regexp(
            params.pop('pattern')
        ))
    if 'enum' in available:
        constraints['choices'] = params.pop('enum')
    if 'minItems' in available:
        constraints['min_entries'] = params.pop('minItems')
    if 'maxItems' in available:
        constraints['max_entries'] = params.pop('maxItems')
    return constraints


class Metadata(TypedDict):
    default: Any
    description: str
    label: str


class Field:
    type_: str
    metadata: Metadata
    required: bool
    readonly: bool = False
    choices: Choices = None
    factory: Optional[wtforms.fields.Field] = None
    subfield: wtforms.fields.Field = None

    def __init__(self, name, required, **params):
        type_ = params.pop('type', None)
        if type_ is None:
            raise KeyError(f'Property of undefined type: {params!r}.')
        if not isinstance(type_, str):
            raise NotImplementedError(
                f"Property {name}: unsupported type '{type_!r}'.")

        self.type_ = type_
        self.required = required
        self.metadata = {
            'default': params.pop('default', None),
            'description': params.pop('descriptions', None),
            'label': params.pop('title', name),
        }
        if (items := params.pop('items', None)) is not None:
            if isinstance(items, list):
                # This is a tuple declaration.
                # Currently unhandled
                raise NotImplementedError(
                    "Array from Tuple is not implemented")
            self.subfield = Field(name, required, **items)
        self.params = params

    def cast(self):
        options = constraints_from_params(self.required, **self.params)
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
        return factory, {**self.metadata, **options}

    def __call__(self):
        factory, options = self.cast()
        return factory(**options)
