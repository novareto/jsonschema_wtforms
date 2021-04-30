import pytest
import hamcrest
import wtforms.form
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import BooleanParameters


def test_boolean():
    field = BooleanParameters.from_json_field('test', True, {
        "type": "boolean",
    })

    constraints = field.get_options()
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
        )
    }))

    assert field.required is True
    assert field.get_factory() == wtforms.fields.BooleanField
    form = wtforms.form.BaseForm({"test": field()})
    form.process(data={'test': 1})
    assert form.validate() is True