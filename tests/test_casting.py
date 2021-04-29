import typing
import wtforms.fields
import wtforms.validators
from jsonschema_wtforms.field import Field, constraints_from_params
from jsonschema_wtforms._fields import MultiCheckboxField


def test_integer_constraints():

    constraints_from_params('test', False, {
        "type": "string",
        "description": "The person's first name."
    })
