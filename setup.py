from setuptools import setup


setup(
    name='jsonschema_wtforms',
    install_requires=[
        'wtforms>=3',
        'jsonschema',
    ],
    extras_require={
        'test': [
            'pytest>=3',
            'PyHamcrest'
        ]
    }
)
