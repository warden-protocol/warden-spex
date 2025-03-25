# ruff: noqa: S602


import os
import shutil
from subprocess import run
from typing import Any

import semver
from colorama import Fore, Style
from dotenv import load_dotenv
from tomlkit import dumps, parse

from warden_spex.pkg import package_name, package_version, project_dir


class RedAssertionError(AssertionError):
    def __str__(self):
        """Returning error message in red color."""
        return f"{Fore.LIGHTRED_EX}{super().__str__()}{Style.RESET_ALL}"


def bump_package_version() -> str:
    """
    Returns package version with patch bump.
    """
    with open(project_dir / "pyproject.toml", "rb") as f:
        data: dict[str, Any] = parse(f.read())

    package_version_from_toml = data["project"]["version"]

    # Make sure that the version from the `pkg` module
    # matches the version reported in the toml file.
    # If they different, something unexpected is happening.
    if package_version != package_version_from_toml:
        raise RedAssertionError(f"Package version not matching with pyproject.toml: {package_version} != {package_version_from_toml}")

    print(f"Current package version: {package_version}")

    bumped_package_version = str(semver.Version.parse(package_version).bump_patch())

    data["project"]["version"] = bumped_package_version

    with open("pyproject.toml", mode="w", encoding="utf-8") as f:
        f.write(dumps(data))

    print(f"Bumped package version: {bumped_package_version}")

    return bumped_package_version


def execute(*args, env: dict[str, str] | None = None, verbose: bool = False):
    """
    Execute `args`, considering `env` environ variables, printing stdout, stderr if `verbose`.
    If the return code is different than zero, raise exception.
    """

    cmd = " ".join([str(arg) for arg in args])
    cp = run(args, text=True, env=env, capture_output=True, check=False)
    if cp.returncode != 0:
        raise RedAssertionError(f"\n\n{cmd}\n\n{cp.stdout}\n\n{Fore.RED}{cp.stderr}{Style.RESET_ALL}\n")
    if verbose:
        print(f"{cmd}\n{cp.stdout}\n{cp.stderr}")


def main():
    """
    Publish package, after running tests, creating package.
    After publishing, the test is also tested for installation.
    """
    os.chdir(project_dir)
    print("Removing ./dist/ ...")
    shutil.rmtree(project_dir / "dist", ignore_errors=True)
    print("Running tests ...")
    execute("uv", "run", "pytest")
    bumped_package_version = bump_package_version()
    print("Building wheel package ...")
    execute("uv", "build", "--wheel", "--no-sources")
    load_dotenv(dotenv_path=".env", override=True)
    print("Publishing ...")
    execute(
        "uv",
        "publish",
        env=os.environ,
    )

    print("Testing published package ...")
    execute(
        "uv",
        "run",
        "--refresh-package",
        package_name,
        "--with",
        package_name,
        "--no-project",
        "--",
        "python",
        "-c",
        f"'from {package_name}.pkg import package_version; assert package_version == \"{bumped_package_version}\"'",
    )

    print(f"\n=== == = . Package {Fore.LIGHTGREEN_EX}{package_name}=={bumped_package_version}{Style.RESET_ALL} published! . - = == ===\n")


if __name__ == "__main__":
    main()
