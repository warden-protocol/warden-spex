from collections.abc import Callable
from subprocess import run

import pytest


def _check_run(*args):
    """
    Execute args on local environment.
    If the return code is non-zero, an exception is raised.
    """

    cmd = " ".join([str(arg) for arg in args])
    cp = run(args, text=True, capture_output=True, check=False)
    assert cp.returncode == 0, f"\n\n{cmd}\n\n{cp.stdout}\n\n{cp.stderr}\n"
    print(cp.stdout)


@pytest.fixture(scope="session")
def check_run() -> Callable:
    return _check_run


def pytest_collection_modifyitems(items: list[pytest.Item]):
    """
    Reorder the tests to ensure that pylint runs last.
    """
    # Separate out the test named 'test123'
    target_items = [item for item in items if item.name == "test_pylint"]
    other_items = [item for item in items if item.name != "test_pylint"]

    # Reassemble the list with test123 at the end
    items[:] = other_items + target_items
