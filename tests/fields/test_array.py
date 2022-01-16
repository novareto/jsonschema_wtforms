import pytest
import wtforms.form
import wtforms.fields
import wtforms.validators
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
        "default": [[1]],
        "items": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    })

    form = wtforms.form.BaseForm({"test": field()})
    form.process()
    assert form._fields['test'].data == field.attributes['default']
    assert form.validate()

    factory = field.get_factory()
    assert factory.func == wtforms.fields.FieldList
    subfield = factory.args[0].field_class
    assert subfield == wtforms.fields.FieldList
    subsubfield = factory.args[0].args[0].field_class
    assert subsubfield == wtforms.fields.FloatField


def test_complex_array_of_objects():

    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "creation-date": {
                    "type": "string",
                    "format": "date"
                },
                "files": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "binary",
                        "contentMediaType": [
                            ".pdf",
                            ".jpg",
                            ".png"
                        ]
                    }
                }
            }
        }
    })

    factory = field.get_factory()
    assert factory.func == wtforms.fields.FieldList
    subfield = factory.args[0].field_class
    assert subfield == wtforms.fields.FormField


def test_files_array():
    field = ArrayParameters.from_json_field('test', True, {
        "type": "array",
        "items": {
            "type": "string",
            "format": "binary",
            "contentMediaType": [
                "image/gif",
                ".jpg",
                ".png"
            ]
        },
        "title": "Some images."
    })
    form = wtforms.form.BaseForm({"test": field()})
    assert form._fields['test']() == (
        '<input accept="image/gif|.jpg|.png" id="test" multiple '
        'name="test" required type="file">'
    )
