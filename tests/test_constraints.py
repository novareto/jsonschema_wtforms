import hamcrest
import wtforms.fields
import wtforms.validators
import jsonschema_wtforms.validators
from jsonschema_wtforms.field import constraints_from_params


def test_length():
    constraints = constraints_from_params(**{
        "minLength": 2,
        "maxLength": 3
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional),
            hamcrest.instance_of(wtforms.validators.Length)
        ),
    }))


def test_pattern():
    constraints = constraints_from_params(**{
        "pattern": "^The "
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional),
            hamcrest.instance_of(wtforms.validators.Regexp)
        ),
    }))


def test_items():

    constraints = constraints_from_params(**{
        "minItems": 1,
        "maxItems": 3
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional)
        ),
        'min_entries': 1,
        'max_entries': 3
    }))

    constraints = constraints_from_params(**{
        "type": "array",
        "items": {
            "type": "string"
        }
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional)
        ),
    }))


def test_enum():
    constraints = constraints_from_params(**{
        "enum": [1, 2, 3]
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional)
        ),
        'choices': [1, 2, 3]
    }))


def test_max_min():
    constraints = constraints_from_params(**{
        "maximum": 19.99
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.Optional),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))

    constraints = constraints_from_params(required=True, **{
        "minimum": 2.99
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))

    constraints = constraints_from_params(required=True, **{
        "exclusiveMinimum": 2,
        "exclusiveMaximum": 15
    })
    hamcrest.assert_that(constraints, hamcrest.has_entries({
        'validators': hamcrest.contains_exactly(
            hamcrest.instance_of(wtforms.validators.DataRequired),
            hamcrest.instance_of(jsonschema_wtforms.validators.NumberRange)
        )
    }))
