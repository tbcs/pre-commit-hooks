# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-markdown", file_name="test.md")

testdata = [
    t(
        True,
        """# Heading

The quick brown fox jumps over the lazy dog.
""",
        """# Heading

The quick brown fox jumps over the lazy dog.
""",
    ),
    t(
        False,
        """#  Heading
The quick brown fox jumps over the lazy dog.
""",
        """# Heading

The quick brown fox jumps over the lazy dog.
""",
    ),
    t(
        False,
        """# Assert that paragraphs get wrapped

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
""",  # noqa: E501
        """# Assert that paragraphs get wrapped

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
""",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
