# ruff: noqa: F403, F405

from .filecheck_hook import *


def t(passes: bool, content: str, file_name: str) -> FileCheckHookTest:
    return FileCheckHookTest(
        passes,
        content,
        modified_content=content,
        hook_id="lint-makefile-suspicious-continuations",
        file_name=file_name,
    )


testdata = [
    t(True, "target:\n\tcommand\n", "Makefile"),
    t(True, "target:\n\tcommand\\\n\t\tcontinuation\n", "Makefile"),
    t(False, "target:\n\tspace at EOL\\ \n\t\tcontinuation\n", "Makefile"),
    t(False, "target:\n\tspace at EOL\\ \n\t\tcontinuation\n", "makefile"),
    t(
        False,
        "target:\n\tspace at EOL\\ \n\t\tcontinuation\n",
        "build.Makefile",
    ),
    t(
        False,
        "target:\n\tspace at EOL\\ \n\t\tcontinuation\n",
        "build.makefile",
    ),
    t(False, "target:\n\tspace at EOL\\ \n\t\tcontinuation\n", "build.mk"),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
