from typing import override

from commitizen.cz.conventional_commits.conventional_commits import (
    ConventionalCommitsCz,
)
from commitizen.defaults import Questions

# How long a line of the body or footer should be before wrapping.
TEXT_WIDTH = 72


class ExtendedConventionalCz(ConventionalCommitsCz):
    @override
    def questions(self) -> Questions:
        questions = list(super().questions())
        prefix_question = questions[0]
        assert (
            prefix_question["name"] == "prefix"
        ), "Expected the first question to be 'prefix'"
        prefix_question["choices"] += [
            {
                "value": "deps",
                "name": "deps: Dependency updates that do not change the behavior; use feat "
                + "changes that cause user-facing changes.",
                "key": "e",
            },
            {
                "value": "chore",
                "name": "chore: General maintenance tasks that do not change the "
                + "behavior",
                "key": "o",
            },
        ]
        prefix_question["choices"].sort(key=lambda c: c["value"])
        return questions

    @override
    def schema_pattern(self) -> str:
        PATTERN = (
            r"(?s)"  # To explicitly make . match new line
            r"(build|chore|ci|deps|docs|feat|fix|perf|refactor|style|test|revert|bump)"  # type
            r"(\(\S+\))?!?:"  # scope
            r"( [^\n\r]+)"  # subject
            r"((\n\n.*)|(\s*))?$"
        )
        return PATTERN
