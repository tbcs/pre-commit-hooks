# ruff: noqa: F403, F405

from .filecheck_hook import *


def t(
    passes: bool, content: str, file_name: str, file_mode: int = 0o644
) -> FileCheckHookTest:
    return FileCheckHookTest(
        passes,
        content,
        modified_content=content,
        hook_id="lint-shell",
        file_name=file_name,
        file_mode=file_mode,
    )


testdata = [
    t(
        True,
        """#!/bin/sh
echo "$1"
""",
        file_name="test.sh",
    ),
    t(
        False,
        """#!/bin/sh
echo $1
""",
        file_name="test.sh",
    ),
    t(
        False,
        """#!/bin/sh
echo $1
""",
        file_name="noext",
        file_mode=0o755,
    ),
    t(
        False,
        """#!/bin/bash
echo $1
""",
        file_name="noext",
        file_mode=0o755,
    ),
    t(
        False,
        """#!/usr/bin/env bash
echo $1
""",
        file_name="noext",
        file_mode=0o755,
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
