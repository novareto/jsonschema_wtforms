import json
import wtforms.form
import pytest
import pathlib


@pytest.fixture(scope="session")
def product_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('product.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def person_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('person.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def address_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('address.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def geo_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('geo.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def refs_and_defs_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('refs_defs.json')
    with config.open() as fp:
        return json.load(fp)


class DummyField:
    data = None

    @property
    def raw_data(self):
        return [self.data]


@pytest.fixture
def dummy_field():
    return DummyField()


@pytest.fixture(scope="function")
def form():
    return wtforms.form.Form()
