import pytest
import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import ArrayParameters


def test_array_without_items():

    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
    })

    with pytest.raises(NotImplementedError) as exc:
        field.get_factory()

    assert str(exc.value) == (
        "Unsupported array type : 'items' attribute required.")


def test_simple_array():

    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
        "items": {
            "type": "number"
        }
    })

    factory = field.get_factory()
    assert factory.func == wtforms.fields.FieldList
    subfield = factory.args[0].field_class
    assert subfield == wtforms.fields.FloatField


def test_array_length():

    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
        "minItems": 2,
        "maxItems": 3,
        "items": {
            "type": "number"
        }
    })

    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': [1, 2, 3]})
    assert form.validate() is True
    assert not form.errors

    # Fixme, this sucks.
    # It probably needs a formdata, to work properly
    with pytest.raises(AssertionError):
        form.process(data={'test': [1, 4, 5, 9]})


def test_complex_array():

    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    })

    factory = field.get_factory()
    assert factory.func == wtforms.fields.FieldList
    subfield = factory.args[0].field_class
    assert subfield == wtforms.fields.core.FieldList
    subsubfield = factory.args[0].args[0].field_class
    assert subsubfield == wtforms.fields.FloatField
