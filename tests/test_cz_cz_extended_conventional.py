import pytest
from commitizen import defaults
from commitizen.config.base_config import BaseConfig

from cz_extended_conventional import ExtendedConventionalCz


# Taken from: https://github.com/commitizen-tools/commitizen/blob/c1884bddbeb6afa0af72c9526e18fac16c46e766/tests/conftest.py#L137
@pytest.fixture()
def config():
    _config = BaseConfig()
    _config.settings.update({"name": defaults.DEFAULT_SETTINGS["name"]})
    return _config


@pytest.fixture
def extended_conventional(config):
    return ExtendedConventionalCz(config)


def test_questions(extended_conventional):
    questions = extended_conventional.questions()
    assert isinstance(questions, list)


@pytest.mark.parametrize(
    "prefix, expected",
    [
        # Test the new prefixes
        ("deps", "deps: Subject of the commit"),
        # Test existing prefixes
        ("feat", "feat: Subject of the commit"),
    ],
)
def test_prefixes(extended_conventional, prefix, expected):
    answers = {
        "prefix": prefix,
        "scope": "",
        "subject": "Subject of the commit",
        "body": "",
        "footer": "",
        "is_breaking_change": False,
    }
    message = extended_conventional.message(answers)
    assert message == expected


@pytest.mark.parametrize(
    "message, expected",
    [
        # Test the new prefixes
        ("chore: General maintenance task", "General maintenance task"),
        ("deps: Update dependencies", "Update dependencies"),
        (
            "deps!: Update important dependencies\n\nTest",
            "Update important dependencies",
        ),
        (
            "deps(component): Update dependencies in component",
            "Update dependencies in component",
        ),
        # Test existing prefixes
        ("feat: Add new feature", "Add new feature"),
        # Test invalid prefix
        ("invalid: This should not match", ""),
    ],
)
def test_schema_pattern(extended_conventional, message, expected):
    result = extended_conventional.process_commit(message)
    assert result == expected
