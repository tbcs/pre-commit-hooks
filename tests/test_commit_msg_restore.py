import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest
from git import Repo
from pre_commit.commands.try_repo import try_repo
from pytest import MonkeyPatch

from .utils import create_run_args


@dataclass(frozen=True)
class CommitMsgRestoreTest:
    backup_message: str | None
    commit_with_editor: bool = True


t = CommitMsgRestoreTest

testdata = [
    t("inline function in FooBar::func"),
    t(None),
    t("inline function in FooBar::func", commit_with_editor=False),
]


@pytest.mark.parametrize("test", testdata)
def test_commit_msg_restore(
    tmp_path: Path,
    project_root_dir: Path,
    test: CommitMsgRestoreTest,
    monkeypatch: MonkeyPatch,
) -> None:
    Repo.init(tmp_path)
    monkeypatch.chdir(tmp_path)

    if not test.commit_with_editor:
        # commit message was supplied via the command line, e.g.:
        #   git commit -m 'message'
        monkeypatch.setenv("GIT_EDITOR", ":")

    # This file, when present, contains the message for a previously attempted
    # commit which failed to pass a `commit-msg` hook check.
    commit_msg_backup_file = Path(".git/COMMIT_EDITMSG.bak")

    # We check this file's content after the `prepare-commit-msg` hook ran.  If
    # there was no previous commit message to restore from a backup file then
    # this file is expected to be unchanged.  If a backed up commit message did
    # exist then this file is expected to contain that message.
    commit_msg_file = Path(".git/COMMIT_EDITMSG")

    # Normal use of a `prepare-commit-msg` hook doesn't require the commit
    # message file to be present.  However, because we use pre-commit's
    # `try-repo` for testing, we have to provide an existing file to
    # `--commit-msg-filename` for the hook not to be skipped.  And since the
    # file has to exist we fill it with some random content, allowing us to
    # later assert that the file wasn't modified -- this is relevant for test
    # cases where a commit message backup is not expected to be restored).
    commit_msg_file_orig_content = str(uuid.uuid4()) + "\n"
    commit_msg_file.write_text(commit_msg_file_orig_content)

    if test.backup_message:
        commit_msg_backup_file.write_text(test.backup_message)

    # run the hook being tested
    args = create_run_args(
        "commit-msg-restore",
        "prepare-commit-msg",
        project_root_dir,
        commit_msg_filename=commit_msg_file,
    )
    return_code = try_repo(args)

    assert return_code == 0

    commit_msg = commit_msg_file.read_text()

    if test.commit_with_editor:
        if test.backup_message:
            assert commit_msg == test.backup_message
        else:
            assert commit_msg == commit_msg_file_orig_content
    else:
        assert commit_msg == commit_msg_file_orig_content
        assert commit_msg_backup_file.exists() is False, (
            "the backup file is deleted if the commit "
            "message was supplied via the command line"
        )
