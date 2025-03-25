# CONTRIBUTING

This guide will help you set up your development environment, manage dependencies, build and test the project, and follow our git workflows. Whether you're adding a feature, fixing a bug, or updating documentation, this guide will get you started quickly and keep your work aligned with the project.

Before you begin: Please open an issue to discuss your contribution. Changes that haven’t been discussed in advance may not be accepted.

## Installing `uv`

* On MacOS, using brew: `brew install uv`
* Or, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/)

## Creating an environment with a specific version of Python

```sh
uv python list # List available and installed versions
uv python install 3.12.8 # Install a specific Python version
uv init --lib --python 3.12.8 # Initializing a new Python project
```

## Adding a dependency

```sh
uv add pandas
```

Adding a dev dependency:

```sh
uv add --dev pytest
```

Updating a package:

```sh
uv lock --upgrade-package pandas
```

Removing a package:

```sh
uv remove pandas
```

## Upgrade all depencencies

```sh
uv lock --upgrade
uv sync
```


## Building the project for distribution

```sh
uv build
```

## Running a command

```sh
uv run jupyter lab       
```

## Bumping the package version (patch)

```sh
uv run python utils/bump_version.py
```
## Publish the project

```sh
uv run python utils/publish_package.py  
```

# Git

## Merging from `main` into `local_branch` branch

```sh
git branch -r # list remote branches
... # select branch you want to merge from . in our case, `main`
git fetch origin main # fetch latest revision of `main` branch
git checkout local_branch # switch to `local_branch`
git merge origin/main # merge `main` into `local_branch`
... # manually resolve conflicts
git add . # add changes
git commit -m "Resolved conflicts" # commit changes
```

To abort a merge: `git merge --abort`

## Unstage changes

```sh
git reset .    
```

## Resolving code health errors

* In case of vulture complaining of unused parameters, you can add the inline comment `# noqa: F841`
* To disable a pylint warning, you can add the inline comment `#pylint: disable=name-of-warning`
* Testing the project/package metadata: `uv run python src/warden_spex/pkg.py`