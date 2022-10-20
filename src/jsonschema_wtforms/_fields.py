import typing as t
from wtforms.utils import unset_value
from wtforms.form import BaseForm
from wtforms.fields import Field, FormField
from wtforms import widgets, SelectMultipleField


Fields = t.Mapping[str, t.Callable[[], Field]]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GenericFormField(FormField):

    fields: t.Mapping[str, t.Callable[[], Field]]

    def __init__(self, fields, form_class=BaseForm, **kwargs):
        self.fields = fields
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=unset_value, extra_filters=None):
        if not extra_filters:
            # We make sure it's None, not empty list or dict.
            extra_filters = None

        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default
            self._obj = data

        self.object_data = data

        prefix = self.name + self.separator
        self.form = self.form_class(
            {name: bind() for name, bind in self.fields.items()},
            prefix=prefix)

        if isinstance(data, dict):
            self.form.process(
                formdata=formdata, extra_filters=extra_filters, **data)
        else:
            self.form.process(
                formdata=formdata, extra_filters=extra_filters, obj=data)

    def validate(self, form, extra_validators=None):
        return self.form.validate(extra_validators=extra_validators)

    @classmethod
    def factory(cls, fields, form_class=BaseForm):
        return GenericFormFactory(cls, fields, form_class)


class GenericFormFactory(t.NamedTuple):
    fields: Fields
    form_class: t.Type[BaseForm] = BaseForm
    form_field: t.Type[GenericFormField] = GenericFormField

    def __call__(self, **kwargs):
        return self.form_field(
            self.fields, form_class=self.form_class, **kwargs)
