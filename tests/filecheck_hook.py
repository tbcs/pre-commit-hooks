import functools
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ParamSpec, TypeVar

import pytest
from git import Repo
from pre_commit.commands.try_repo import try_repo
from pytest import CaptureFixture, FixtureRequest, MonkeyPatch

from .assertions import assert_hook_result
from .utils import create_run_args

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class FileCheckHookTest:
    passes: bool
    content: str
    modified_content: str
    hook_id: str
    file_name: str
    file_mode: int = 0o644


def filecheck_hook_test(
    data: Sequence[FileCheckHookTest],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @pytest.mark.usefixtures("run_filecheck_hook_test")
        @pytest.mark.parametrize(
            "run_filecheck_hook_test", data, indirect=True, ids=range(len(data))
        )
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.fixture
def run_filecheck_hook_test(
    request: FixtureRequest,
    capfd: CaptureFixture[str],
    tmp_path: Path,
    project_root_dir: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    git_repo = Repo.init(tmp_path)
    monkeypatch.chdir(tmp_path)

    test = request.param

    test_file = Path(test.file_name)

    # create the file to be checked in the test git repository
    test_file.write_text(test.content)
    test_file.chmod(test.file_mode)
    git_repo.index.add([test_file])

    # run the hook being tested, capturing pre-commit's output
    args = create_run_args(
        test.hook_id, "pre-commit", project_root_dir, [test_file]
    )
    return_code = try_repo(args)
    (output, _) = capfd.readouterr()

    # get the test file's content (possibly modified by the hook)
    file_content = test_file.read_text()

    assert_modification(test, output, file_content)
    assert_hook_result(test.passes, return_code)


def assert_modification(
    test: FileCheckHookTest,
    precommit_output: str,
    file_content: str,
) -> None:
    assert test.modified_content == file_content
    if test.modified_content == test.content:
        return
    assert (
        f"hook id: {test.hook_id}\n- files were modified by this hook\n"
        in precommit_output
    )
