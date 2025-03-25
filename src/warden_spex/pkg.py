from importlib.metadata import version as metadata_version
from pathlib import Path

project_dir = Path(__file__).parent.parent.parent.resolve()
package_name = Path(__file__).parent.name
package_version = metadata_version(package_name)


def main():
    print(f"project_dir........: {project_dir}")
    print(f"package_name.......: {package_name}")
    print(f"package_version....: {package_version}")


if __name__ == "__main__":
    main()
