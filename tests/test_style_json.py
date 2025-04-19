# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-json", file_name="test.json")

testdata = [
    t(
        True,
        """{
  "foo": true
}
""",
        """{
  "foo": true
}
""",
    ),
    t(
        False,
        """{
"foo": true
}
""",
        """{
  "foo": true
}
""",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
