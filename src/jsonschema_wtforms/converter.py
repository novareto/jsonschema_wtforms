import abc
import wtforms.fields
import wtforms.validators
from typing import List, Dict, Type, ClassVar, Tuple, Optional


class NotRequired(wtforms.validators.Optional):

    def __call__(self, form, field):
        if entries := getattr(field, 'entries', None):
            return
        return super().__call__(form, field)


class JSONFieldParameters(abc.ABC):
    supported: ClassVar[set]
    ignore: ClassVar[set] = {
        'additionalProperties', 'name', 'type',
        'title', 'description', 'anyOf', 'if', 'then'
    }
    allowed: ClassVar[set] = frozenset(('default',))

    type: str
    name: str
    label: str
    description: str
    validators: List
    attributes: Dict
    required: bool
    factory: Optional[Type[wtforms.fields.Field]] = None

    def __init__(self,
                 type: str,
                 name: str,
                 required: bool,
                 validators: List,
                 attributes: Dict,
                 label: str = '',
                 description: str = ''):
        if type not in self.supported:
            raise TypeError(
                f'{self.__class__} does not support the {type} type.')
        self.type = type
        self.name = name
        self.label = label or name
        self.description = description
        self.required = required
        self.validators = validators
        self.attributes = attributes

    def get_options(self):
        return {
            'label': self.label,
            'description': self.description,
            'validators': [
                wtforms.validators.DataRequired() if self.required else
                NotRequired(), *self.validators
            ], **self.attributes
        }

    @abc.abstractmethod
    def get_factory(self):
        return self.factory

    def __call__(self):
        options = self.get_options()
        factory = self.get_factory()
        return factory(**options)

    def bind(self, form, **options):
        wtfield = self()
        return wtfield.bind(form, **options)

    @classmethod
    def extract(cls, params: dict, available: set) -> Tuple[List, Dict]:
        return [], {}

    @classmethod
    def from_json_field(cls, name: str, required: bool, params: dict):
        available = set(params.keys())
        if illegal := ((available - cls.ignore) - cls.allowed):
            raise NotImplementedError(
                f'Unsupported attributes: {illegal} for {cls}.')
        validators, attributes = cls.extract(params, available)
        return cls(
            params['type'],
            name,
            required,
            validators,
            attributes,
            label=params.get('title'),
            description=params.get('description')
        )


class Converter:

    converter: Dict[str, JSONFieldParameters]

    def __init__(self):
        self.converters = {}

    def register(self, type: str):
        def type_registration(converter: JSONFieldParameters):
            self.converters[type] = converter
            return converter
        return type_registration

    def lookup(self, type: str, defs: dict = None):
        return self.converters[type]


converter = Converter()
