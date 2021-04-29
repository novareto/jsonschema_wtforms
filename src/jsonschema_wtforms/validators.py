import math
from wtforms.validators import ValidationError


class NumberRange:

    def __init__(self,
                 min=None,
                 max=None,
                 exclusive_min=False,
                 exclusive_max=False,
                 message=None):
        self.min = min
        self.max = max
        self.exclusive_min=False,
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
            if self.min is not None and (
                    self.exclusive_min and data > self.min
                    or data >= self.min):
                return
            if self.max is not None and (
                    self.exclusive_max and data < self.max
                    or data <= self.max):
                return

        if self.message is not None:
            message = self.message

        # we use %(min)s interpolation to support floats, None, and
        # Decimals without throwing a formatting exception.
        elif self.max is None:
            message = field.gettext("Number must be at least %(min)s.")

        elif self.min is None:
            message = field.gettext("Number must be at most %(max)s.")

        else:
            message = field.gettext("Number must be between %(min)s and %(max)s.")

        raise ValidationError(message % dict(min=self.min, max=self.max))
