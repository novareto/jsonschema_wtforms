import json
import pytest
import pathlib


@pytest.fixture
def product_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('product.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture
def person_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('person.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture
def address_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('address.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture
def geo_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('geo.json')
    with config.open() as fp:
        return json.load(fp)


@pytest.fixture
def refs_and_defs_schema():
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('refs_defs.json')
    with config.open() as fp:
        return json.load(fp)
