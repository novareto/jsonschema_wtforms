import math
from wtforms.validators import ValidationError


class NumberRange:

    def __init__(self,
                 min=None,
                 max=None,
                 exclusive_min=None,
                 exclusive_max=None,
                 message=None):
        self.min = min
        self.max = max
        self.exclusive_min=False
        self.exclusive_max=False
        self.message = message
        self.field_flags = {}
        if self.min is not None:
            self.field_flags["min"] = self.min
        if self.max is not None:
            self.field_flags["max"] = self.max

    def __call__(self, form, field):
        data = field.data
        if data is not None and not math.isnan(data):
            try:
                if self.min is not None and data < self.min:
                    raise ValidationError(
                        field.gettext("Number must be at least %(min)s.")
                        % self.min
                    )
                if self.exclusive_min and data <= self.min:
                    raise ValidationError(
                        field.gettext("Number must be over %(min)s.")
                        % self.exclusive_min
                    )
                if self.max is not None and data > self.max:
                    raise ValidationError(
                        field.gettext("Number must be at most %(max)s.")
                        % self.max
                    )
                if self.exclusive_max and data >= self.max:
                    raise ValidationError(
                        field.gettext("Number must be under %(max)s.")
                        % self.exclusive_max
                    )
            except ValidationError:
                if self.message:
                    raise ValidationError(message)
                raise
