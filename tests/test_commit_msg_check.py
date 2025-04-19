from dataclasses import dataclass
from pathlib import Path

import pytest
from git import Repo
from pre_commit.commands.try_repo import try_repo
from pytest import MonkeyPatch

from .assertions import assert_hook_result
from .utils import create_run_args


@dataclass(frozen=True)
class CommitlintTest:
    passes: bool
    message: str
    cfg_yaml: str


configs = {
    "simple": """#
rules:
  header-max-length: [2, always, 80]
""",
    "conventionalcommits": """#
extends: ["@commitlint/config-conventional"]
rules:
  type-enum: [2, always, [refactor, custom]]
""",
}

t = CommitlintTest

testdata = [
    t(True, "inline function in FooBar::func", cfg_yaml=configs["simple"]),
    t(
        False,
        "inline function in FooBar::func"
        " in order to eliminate the function call "
        "overhead and thus improve performance",
        cfg_yaml=configs["simple"],
    ),
    t(
        True,
        "refactor: inline function in FooBar::func",
        cfg_yaml=configs["conventionalcommits"],
    ),
    t(
        True,
        "custom: inline function in FooBar::func",
        cfg_yaml=configs["conventionalcommits"],
    ),
    t(
        False,
        "inline function in FooBar::func",
        cfg_yaml=configs["conventionalcommits"],
    ),
]


@pytest.mark.parametrize("test", testdata)
def test_commit_msg_check(
    tmp_path: Path,
    project_root_dir: Path,
    test: CommitlintTest,
    monkeypatch: MonkeyPatch,
) -> None:
    git_repo = Repo.init(tmp_path)
    monkeypatch.chdir(tmp_path)

    commitlint_cfg_file = ".commitlintrc.yml"
    Path(commitlint_cfg_file).write_text(test.cfg_yaml)
    git_repo.index.add([commitlint_cfg_file])
    git_repo.index.commit("initial commit", skip_hooks=True)

    commit_msg_file = Path(".git/COMMIT_EDITMSG")
    commit_msg_file.write_text(test.message)

    # run the hook being tested
    args = create_run_args(
        "commit-msg-check",
        "commit-msg",
        project_root_dir,
        commit_msg_filename=commit_msg_file,
    )
    return_code = try_repo(args)

    assert_hook_result(test.passes, return_code)
