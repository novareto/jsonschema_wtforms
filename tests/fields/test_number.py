import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import NumberParameters


def test_max():
    field = NumberParameters.from_json_field('test', True, {
        "type": "integer",
        "maximum": 20
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.IntegerField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 21})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be at most 20.']}

    form.process(data={'test': 12})
    assert form.validate() is True
    assert not form.errors


def test_min():
    field = NumberParameters.from_json_field('test', True, {
        "type": "number",
        "minimum": 2.99
    })
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))
    assert field.required is True
    assert field.get_factory() == wtforms.fields.FloatField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 2.10})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be at least 2.99.']}

    form.process(data={'test': 12})
    assert form.validate() is True
    assert not form.errors


def test_exclusive_minmax():

    field = NumberParameters.from_json_field('test', True, {
        "type": "integer",
        "exclusiveMinimum": 2,
        "exclusiveMaximum": 15
    })
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))
    assert field.required is True
    assert field.get_factory() == wtforms.fields.IntegerField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 1})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be over 2.']}

    form.process(data={'test': 2})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be over 2.']}

    form.process(data={'test': 16})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be under 15.']}

    form.process(data={'test': 15})
    assert form.validate() is False
    assert form.errors == {'test': ['Number must be under 15.']}

    form.process(data={'test': 10})
    assert form.validate() is True
    assert not form.errors


def test_enum():
    field = NumberParameters.from_json_field('test', True, {
        "type": "integer",
        "enum": [1, 2]
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.SelectField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 9})
    assert form.validate() is False
    assert form.errors == {'test': ['Not a valid choice.']}

    form.process(data={'test': 1})
    assert form.validate() is True
    assert not form.errors
