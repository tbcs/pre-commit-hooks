def assert_hook_result(success_expected: bool, precommit_rc: int) -> None:
    hook_success = precommit_rc == 0
    if success_expected:
        assert hook_success, "hook failed, but was expected to pass"
    else:
        assert not hook_success, "hook passed, but was expected to fail"
