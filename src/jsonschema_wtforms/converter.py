import abc
import wtforms.fields
import wtforms.validators
from typing import List, Dict, Literal, Type, ClassVar, Tuple, Optional


class JSONFieldParameters(abc.ABC):
    type: str
    name: str
    validators: List
    attributes: Dict
    required: bool
    factory: Optional[Type[wtforms.fields.Field]] = None
    supported: ClassVar[set]
    ignore: ClassVar[set] = frozenset(('type', 'title', 'description'))
    allowed: ClassVar[set] = frozenset()

    def __init__(self, type: str, name: str, required: bool,
                 validators: List, attributes: Dict):
        if type not in self.supported:
            raise TypeError(
                f'{self.__class__} does not support the {type} type.')
        self.type = type
        self.name = name
        self.required = required
        self.validators = validators
        self.attributes = attributes

    def get_options(self):
        return {
            'validators': [
                wtforms.validators.DataRequired() if self.required else
                wtforms.validators.Optional(), *self.validators
            ], **self.attributes
        }

    @abc.abstractmethod
    def get_factory(self):
        return self.factory

    def __call__(self):
        options = self.get_options()
        factory = self.get_factory()
        return factory(**options)

    @classmethod
    def extract(cls, params: dict, available: str) -> Tuple[List, Dict]:
        return [], {}

    @classmethod
    def from_json_field(cls, name: str, required: bool, params: dict):
        available = set(params.keys())
        if illegal := ((available - cls.ignore) - cls.allowed):
            raise NotImplementedError(
                f'Unsupported attributes for string type: {illegal}')
        return cls(
            params['type'], name, required,
            *cls.extract(params, available)
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
