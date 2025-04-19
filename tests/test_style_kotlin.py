# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-kotlin")

testdata = [
    t(
        True,
        """//
val foo = "bar"
""",
        """//
val foo = "bar"
""",
        file_name="test.kt",
    ),
    t(
        False,
        """//
val foo   = "bar"
""",
        """//
val foo = "bar"
""",
        file_name="test.kt",
    ),
    t(
        False,
        """//
val foo   = "bar"
""",
        """//
val foo = "bar"
""",
        file_name="test.kts",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
