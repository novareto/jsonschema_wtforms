import contextvars
import typing as t
import wtforms.fields
from jsonschema_wtforms._fields import MultiCheckboxField, GenericFormField


class FieldPolicy(t.NamedTuple):
    generic: t.Mapping[str, wtforms.fields.Field]
    formats: t.Mapping[str, wtforms.fields.Field]


BASE_FIELD_POLICY = FieldPolicy(
    generic={
        'choice': wtforms.fields.SelectField,
        'integer': wtforms.fields.IntegerField,
        'float': wtforms.fields.FloatField,
        'boolean': wtforms.fields.BooleanField,
        'array': wtforms.fields.FieldList,
        'object': GenericFormField,
        'multi_file': wtforms.fields.MultipleFileField,
        'multi_choice': MultiCheckboxField,
    },
    formats={
        'default': wtforms.fields.StringField,
        'password': wtforms.fields.PasswordField,
        'date': wtforms.fields.DateField,
        'time': wtforms.fields.TimeField,
        'date-time': wtforms.fields.DateTimeField,
        'email': wtforms.fields.EmailField,
        'ipv4': wtforms.fields.StringField,
        'ipv6': wtforms.fields.StringField,
        'binary': wtforms.fields.FileField,
        'uri': wtforms.fields.URLField
    }
)


Policy = contextvars.ContextVar('FieldPolicy', default=BASE_FIELD_POLICY)
