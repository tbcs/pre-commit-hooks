# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-shell")

testdata = [
    t(
        True,
        """#
if true; then
  exit 0
fi
""",
        """#
if true; then
  exit 0
fi
""",
        file_name="test.sh",
    ),
    t(
        False,
        """#
if true; then
exit 0
fi
""",
        """#
if true; then
  exit 0
fi
""",
        file_name="test.sh",
    ),
    t(
        False,
        """#!/bin/sh
if true; then
exit 0
fi
""",
        """#!/bin/sh
if true; then
  exit 0
fi
""",
        file_name="noext",
        file_mode=0o755,
    ),
    t(
        False,
        """#!/bin/bash
if true; then
exit 0
fi
""",
        """#!/bin/bash
if true; then
  exit 0
fi
""",
        file_name="noext",
        file_mode=0o755,
    ),
    t(
        False,
        """#!/usr/bin/env bash
if true; then
exit 0
fi
""",
        """#!/usr/bin/env bash
if true; then
  exit 0
fi
""",
        file_name="noext",
        file_mode=0o755,
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
