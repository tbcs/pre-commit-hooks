from argparse import Namespace
from pathlib import Path


def create_run_args(  # noqa: PLR0913
    hook_id: str,
    hook_stage: str,
    hooks_repo_dir: Path,
    files: list[Path] | None = None,
    commit_msg_filename: Path | None = None,
    config: str = ".pre-commit-config.yaml",
) -> Namespace:
    """Create an argument namespace for use with `pre_commit.commands.try_repo`.

    This mimics the result of parsing arguments from the command line when
    running `pre-commit try-repo`.

    Args:
        hook_id: The ID of the pre-commit hook to run.
        hook_stage: The stage at which the hook is run (e.g. 'pre-push').
        hooks_repo_dir: Path to the pre-commit hooks repository directory.
        files: List of files to run the hook on.
        commit_msg_filename: File containing the commit message (used at the
            'commit-msg' hook stage).
        config: Path to the pre-commit configuration file.

    Returns:
        An `argparse.Namespace` object configured for the `try-repo` command.
    """
    return Namespace(
        command="try-repo",
        config=config,
        repo=str(hooks_repo_dir),
        ref=None,
        hook=hook_id,
        files=[str(f) for f in files] if files else None,
        all_files=False,
        color=False,
        verbose=False,
        show_diff_on_failure=False,
        hook_stage=hook_stage,
        remote_branch=None,
        local_branch=None,
        from_ref=None,
        to_ref=None,
        pre_rebase_upstream=None,
        pre_rebase_branch=None,
        commit_msg_filename=str(commit_msg_filename),
        prepare_commit_message_source=None,
        commit_object_name=None,
        remote_name=None,
        remote_url=None,
        checkout_type=None,
        is_squash_merge=None,
        rewrite_command=None,
    )
