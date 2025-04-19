# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-java", file_name="test.java")

testdata = [
    t(
        True,
        """//
class Foo {}
""",
        """//
class Foo {}
""",
    ),
    t(
        False,
        """//
class Foo {  }
""",
        """//
class Foo {}
""",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
