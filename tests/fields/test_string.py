import pytest
import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import StringParameters


def test_unknown_format():
    with pytest.raises(NotImplementedError):
        StringParameters.from_json_field('test', True, {
            "type": "string",
            "format": "foobar"
        })


def test_email_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "email"
    })
    assert field.get_factory() == wtforms.fields.html5.EmailField


def test_date_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "date"
    })
    assert field.get_factory() == wtforms.fields.html5.DateField


def test_time_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "time"
    })
    assert field.get_factory() == wtforms.fields.html5.TimeField


def test_datetime_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "date-time"
    })
    assert field.get_factory() == wtforms.fields.html5.DateTimeField


def test_IP_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "ipv4"
    })
    assert field.get_factory() == wtforms.fields.StringField
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(wtforms.validators.IPAddress)
        ),
    }))

    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "ipv6"
    })
    assert field.get_factory() == wtforms.fields.StringField
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(wtforms.validators.IPAddress)
        ),
    }))


def test_length():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "minLength": 1,
        "maxLength": 5
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(wtforms.validators.Length)
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.StringField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 'administrator'})
    assert form.validate() is False
    assert form.errors == {'test': [
        'Field must be between 1 and 5 characters long.'
    ]}

    form.process(data={'test': 'admin'})
    assert form.validate() is True
    assert not form.errors


def test_pattern():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "pattern": "^The"
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(wtforms.validators.Regexp)
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.StringField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 'Dagger'})
    assert form.validate() is False
    assert form.errors == {'test': ['Invalid input.']}

    form.process(data={'test': 'The dagger'})
    assert form.validate() is True
    assert not form.errors


def test_enum():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "enum": ['foo', 'bar']
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.core.SelectField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 'Dagger'})
    assert form.validate() is False
    assert form.errors == {'test': ['Not a valid choice']}

    form.process(data={'test': 'foo'})
    assert form.validate() is True
    assert not form.errors


def test_unhandled_attribute():
    with pytest.raises(NotImplementedError) as exc:
        StringParameters.from_json_field('test', True, {
            "type": "string",
            "unknown": ['foo', 'bar'],
            "pattern": "^f"
        })

    assert str(exc.value) == (
        "Unsupported attributes for string type: {'unknown'}")
