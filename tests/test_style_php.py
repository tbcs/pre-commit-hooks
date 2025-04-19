# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-php", file_name="test.php")

testdata = [
    t(
        True,
        """<?php
function foo(): bool
{
    return true;
}
""",
        """<?php
function foo(): bool
{
    return true;
}
""",
    ),
    t(
        False,
        """<?php
function foo(): bool
{
return true;
}
""",
        """<?php
function foo(): bool
{
    return true;
}
""",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
