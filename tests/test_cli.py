import os
import shutil

from typer.testing import CliRunner

from src.su6.cli import _check_tool, app
from src.su6.core import EXIT_CODE_COMMAND_NOT_FOUND

runner = CliRunner()

from ._shared import BAD_CODE, EXAMPLES_PATH, GOOD_CODE


def test_ruff_good():
    result = runner.invoke(app, ["ruff", GOOD_CODE])
    assert result.exit_code == 0


def test_ruff_bad():
    result = runner.invoke(app, ["ruff", BAD_CODE])
    assert result.exit_code == 1


def test_black_good():
    result = runner.invoke(app, ["black", GOOD_CODE])
    assert result.exit_code == 0


def test_black_bad():
    result = runner.invoke(app, ["black", BAD_CODE])
    assert result.exit_code == 1


def test_black_fix():
    fixable_code = str(EXAMPLES_PATH / "fix_black.py")
    shutil.copyfile(BAD_CODE, fixable_code)
    try:
        # 1. assert error
        result = runner.invoke(app, ["black", fixable_code])
        assert result.exit_code == 1

        # 2. fix
        result = runner.invoke(app, ["--verbosity", "3", "black", fixable_code, "--fix"])
        assert result.exit_code == 0

        # 3. assert success
        result = runner.invoke(app, ["black", fixable_code])
        assert result.exit_code == 0
    finally:
        # cleanup
        os.unlink(fixable_code)


def test_mypy_good():
    result = runner.invoke(app, ["mypy", GOOD_CODE])
    assert result.exit_code == 0


def test_mypy_bad():
    result = runner.invoke(app, ["mypy", BAD_CODE])
    assert result.exit_code == 1


def test_bandit_good():
    result = runner.invoke(app, ["bandit", GOOD_CODE])
    assert result.exit_code == 0


def test_bandit_bad():
    result = runner.invoke(app, ["bandit", BAD_CODE])
    assert result.exit_code == 1


def test_isort_good():
    result = runner.invoke(app, ["isort", GOOD_CODE])
    assert result.exit_code == 0


def test_isort_bad():
    result = runner.invoke(app, ["isort", BAD_CODE])
    assert result.exit_code == 1


def test_isort_fix():
    fixable_code = str(EXAMPLES_PATH / "fix_isort.py")
    shutil.copyfile(BAD_CODE, fixable_code)
    try:
        # 1. assert error
        result = runner.invoke(app, ["isort", fixable_code])
        assert result.exit_code == 1

        # 2. fix
        result = runner.invoke(app, ["--verbosity", "3", "isort", fixable_code, "--fix"])
        assert result.exit_code == 0

        # 3. assert success
        result = runner.invoke(app, ["isort", fixable_code])
        assert result.exit_code == 0
    finally:
        # cleanup
        os.unlink(fixable_code)


def test_all_fix():
    fixable_code = str(EXAMPLES_PATH / "fix_all.py")
    shutil.copyfile(BAD_CODE, fixable_code)
    try:
        # 1. assert error
        result = runner.invoke(app, ["isort", fixable_code])
        assert result.exit_code == 1

        result = runner.invoke(app, ["black", fixable_code])
        assert result.exit_code == 1

        # 2. fix
        result = runner.invoke(app, ["--verbosity", "3", "fix", fixable_code, "--ignore-uninstalled"])
        assert result.exit_code == 0

        # 3. assert success
        result = runner.invoke(app, ["isort", fixable_code])
        assert result.exit_code == 0

        result = runner.invoke(app, ["black", fixable_code])
        assert result.exit_code == 0
    finally:
        # cleanup
        os.unlink(fixable_code)


def test_pydocstyle_good():
    result = runner.invoke(app, ["pydocstyle", GOOD_CODE])
    assert result.exit_code == 0


def test_pydocstyle_bad():
    result = runner.invoke(app, ["pydocstyle", BAD_CODE])
    assert result.exit_code == 1


def test_all_good():
    result = runner.invoke(app, ["--config", str(EXAMPLES_PATH / "except_pytest.toml"), "all", GOOD_CODE])
    assert result.exit_code == 0

    result = runner.invoke(app, ["--config", str(EXAMPLES_PATH / "except_pytest.toml"), "all", GOOD_CODE,
                                 "--ignore-uninstalled"])
    # can't really test without having everything installed,
    # but at least we can make sure the flag doen't crash anything!
    assert result.exit_code == 0


def test_all_bad():
    result = runner.invoke(app, ["--config", str(EXAMPLES_PATH / "except_pytest.toml"), "all", BAD_CODE])
    assert result.exit_code == 1


### test_pytest is kind of an issue since this seems to hang the first running pytest session


def test_command_not_found():
    fake_tool = _check_tool("xxx-should-never-exist-xxx")

    assert fake_tool == EXIT_CODE_COMMAND_NOT_FOUND


def test_custom_include_exclude():
    code_file = str(EXAMPLES_PATH / "black_good_mypy_bad.py")

    result = runner.invoke(app, ["--config", str(EXAMPLES_PATH / "only_black.toml"), "all", code_file])
    assert result.exit_code == 0

    result = runner.invoke(app, ["--config", str(EXAMPLES_PATH / "only_mypy.toml"), "all", code_file])
    assert result.exit_code == 1