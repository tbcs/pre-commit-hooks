# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-yaml")

testdata = [
    t(
        True,
        """#
foo: ["bar"]
""",
        """#
foo: ["bar"]
""",
        file_name="test.yaml",
    ),
    t(
        False,
        """#
foo: [ "bar" ]
""",
        """#
foo: ["bar"]
""",
        file_name="test.yaml",
    ),
    t(
        False,
        """#
foo: [ "bar" ]
""",
        """#
foo: ["bar"]
""",
        file_name="test.yml",
    ),
    t(
        True,
        """#
foo:
  - this test asserts that lines do not get wrapped by the formatter no matter how ridiculously long they are even when readability suffers because yaml is simply too generic for a formatter to enforce a column limit therefore we assume that another hook checks for long lines but we leave it to the user to perform manual wrapping
""",  # noqa: E501
        """#
foo:
  - this test asserts that lines do not get wrapped by the formatter no matter how ridiculously long they are even when readability suffers because yaml is simply too generic for a formatter to enforce a column limit therefore we assume that another hook checks for long lines but we leave it to the user to perform manual wrapping
""",  # noqa: E501
        file_name="test.yaml",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
