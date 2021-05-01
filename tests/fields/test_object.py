import pytest
import wtforms.form
import wtforms.fields
import wtforms.validators
from jsonschema_wtforms.field import ObjectParameters


def test_object():

    with pytest.raises(NotImplementedError):
        field = ObjectParameters.from_json_field('test', True, {
            "type": "object",
        })

    field = ObjectParameters.from_json_field('test', True, {
        "type": "object",
        "properties": {
            "fruits": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    })

    factory = field.get_factory()
    assert factory.func == wtforms.fields.FormField
