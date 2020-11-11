import pytest

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}


@pytest.fixture()
def fake_fixture():
    pass


def test_fake(fake_fixture):
    pass