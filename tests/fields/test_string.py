import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import Field


def test_length():
    field = Field('test', required=True, **{
        "type": "string",
        "minLength": 1,
        "maxLength": 5
    })
    assert field.required == True
    assert field.metadata == {
        'default': None,
        'description': None,
        'label': 'test'
    }
    factory, options = field.cast()
    assert factory == wtforms.fields.StringField
    form = wtforms.form.BaseForm({"test": factory(**options)})
    form.process(data={'test': 'administrator'})
    assert form.errors == {}


def test_pattern():
    field = Field('test', required=False, **{
        "type": "string",
        "pattern": r"^\w+$"
    })
    assert field.required == False
    assert field.metadata == {
        'default': None,
        'description': None,
        'label': 'test'
    }
    factory, options = field.cast()
    assert factory == wtforms.fields.StringField
