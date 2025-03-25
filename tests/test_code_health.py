from warden_spex.pkg import project_dir


def test_mypy(check_run):
    """Test: types validation."""
    check_run("mypy", project_dir)


def test_vulture(check_run):
    """Test: there is no unused code."""
    check_run("vulture", project_dir / "src")


def test_ruff(check_run):
    """Test: lint/autofix/check code with ruff."""
    check_run("ruff", "check", project_dir, "--fix", "--exit-zero")
    check_run("ruff", "format", project_dir)
    check_run("ruff", "check", project_dir, "--quiet")


def test_pylint(check_run):
    """Test: lint with Pylint."""
    check_run("pylint", project_dir / "src", project_dir / "utils", project_dir / "tests")
