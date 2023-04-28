import pytest
import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
from jsonschema_wtforms.field import StringParameters, EnumParameters


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
    assert field.get_factory() == wtforms.fields.EmailField


def test_date_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "date"
    })
    assert field.get_factory() == wtforms.fields.DateField


def test_time_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "time"
    })
    assert field.get_factory() == wtforms.fields.TimeField


def test_datetime_format():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "date-time"
    })
    assert field.get_factory() == wtforms.fields.DateTimeField


def test_uri_format():
    field = StringParameters.from_json_field('test', True, {
        "minLength": 1,
        "maxLength": 2083,
        "format": "uri",
        "type": "string"
    })
    assert field.get_factory() == wtforms.fields.URLField
    form = wtforms.form.BaseForm({"test": field()})
    form.process()
    assert form._fields['test']() == (
        '<input id="test" maxlength="2083" minlength="1" '
        'name="test" required type="url" value="">'
    )


def test_password_format():
    field = StringParameters.from_json_field('test', True, {
        "title": "Password",
        "type": "string",
        "writeOnly": True,
        "format": "password"
    })
    assert field.get_factory() == wtforms.fields.PasswordField
    form = wtforms.form.BaseForm({"test": field()})
    form.process()
    assert form._fields['test']() == (
        '<input id="test" '
        'name="test" required type="password" value="">'
    )


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


def test_binary():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "format": "binary",
        "contentMediaType": [
            ".pdf",
            "image/png"
        ]
    })
    assert field.get_factory() == wtforms.fields.simple.FileField
    form = wtforms.form.BaseForm({"test": field()})
    assert form._fields['test']() == (
        '<input accept=".pdf,image/png" id="test" name="test" '
        'required type="file">'
    )


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
        "pattern": "^The",
        "default": "The "
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(wtforms.validators.Regexp)
        ),
    }))

    assert field.required is True
    assert field.attributes['default']
    assert field.get_factory() == wtforms.fields.StringField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 'Dagger'})
    assert form.validate() is False
    assert form.errors == {'test': ['Invalid input.']}

    form.process(data={'test': 'The dagger'})
    assert form.validate() is True
    assert not form.errors
    form.process()
    assert form._fields['test']() == (
        '<input id="test" name="test" required type="text" value="The ">'
    )


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
    assert field.get_factory() == wtforms.fields.SelectField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 'Dagger'})
    assert form.validate() is False
    assert form.errors == {'test': ['Not a valid choice.']}

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
        "Unsupported attributes: {'unknown'} for "
        "<class 'jsonschema_wtforms.field.StringParameters'>."
    )


def test_anyof():
    field = StringParameters.from_json_field('test', True, {
        "type": "string",
        "oneOf": [
            {"const": "0", "title": "männlich"},
            {"const": "1", "title": "weiblich"},
            {"const": "2", "title": "unbekannt"},
        ]
    })
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.SelectField
    assert field.attributes == {
        'choices': [
            ('0', 'männlich'),
            ('1', 'weiblich'),
            ('2', 'unbekannt')
        ]
    }

def test_enum_anyof():
    field = EnumParameters.from_json_field('test', True, {
        "type": "enum",
        "oneOf": [
            {"const": "0", "title": "männlich"},
            {"const": "1", "title": "weiblich"},
            {"const": "2", "title": "unbekannt"},
        ]
    })
    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
        ),
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.SelectField
    assert field.attributes == {
        'choices': [
            ('0', 'männlich'),
            ('1', 'weiblich'),
            ('2', 'unbekannt')
        ]
    }
