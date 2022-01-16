import pytest
import wtforms.form
import wtforms.fields
import wtforms.validators
from wtforms import FormField

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
    assert False


def test_ref_object():
    root_field = ObjectParameters.from_json_field('test', True, {
        "type": "object",
        "properties": {
            "name": {
                "title": "Name",
                "type": "string"
            },
            "address": {
                "$ref": "#/definitions/Address"
            },
            "devices": {
                "title": "Devices",
                "type": "array",
                "items": {
                    "$ref": "#/definitions/Device"
                }
            }
        },
        "required": [
            "name",
        ],
        "definitions": {
            "Address": {
                "title": "Address",
                "type": "object",
                "properties": {
                    "street": {
                        "title": "Street",
                        "type": "string"
                    },
                    "city": {
                        "title": "City",
                        "type": "string"
                    },
                    "phone": {
                        "title": "Phone",
                        "type": "string"
                    }
                },
                "required": [
                    "street",
                    "city",
                    "phone"
                ]
            },
            "Device": {
                "title": "Device",
                "type": "object",
                "properties": {
                    "kind": {
                        "title": "Kind",
                        "enum": [
                            "PC",
                            "Laptop"
                        ],
                        "type": "string"
                    }
                },
                "required": [
                    "kind"
                ]
            }
        }
    })
    assert root_field.label == 'test'
    assert not root_field.description
    addr = root_field.fields['address']
    assert addr.label == 'Address'
    assert not addr.required

    form = wtforms.form.BaseForm({"address": addr()})
    form.process(data={'address': ''})
    assert not form.validate()
    assert form.errors == {'address': {
        'city': ['This field is required.'],
        'phone': ['This field is required.'],
        'street': ['This field is required.'],
    }}
    form.process(
        data={'address': {'city': 'Boppelsen', 'phone': '666', 'street': 'A'}}
    )
    assert form.validate()

    devices = root_field.fields['devices']
    assert devices.label == 'Devices'
    assert devices.name == 'devices'
    assert not devices.required


