# ruff: noqa: F403, F405

from .filecheck_hook import *


def t(passes: bool, content: str, file_name: str) -> FileCheckHookTest:
    return FileCheckHookTest(
        passes,
        content,
        modified_content=content,
        hook_id="lint-makefile-suspicious-lines",
        file_name=file_name,
    )


testdata = [
    t(True, "target:\n\tcommand\n", "Makefile"),
    t(False, "target:\n \tcommand with mixed space/tab indent\n", "Makefile"),
    t(False, "target:\n\tcommand\n\t", "Makefile"),  # trailing tab and EOF
    t(False, "target:\n\tcommand\n\t", "makefile"),
    t(False, "target:\n\tcommand\n\t", "build.Makefile"),
    t(False, "target:\n\tcommand\n\t", "build.makefile"),
    t(False, "target:\n\tcommand\n\t", "build.mk"),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
