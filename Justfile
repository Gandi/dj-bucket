package := 'dj_bucket'
default_test_suite := 'tests'

[doc("Install dependencies for development purpose")]
install:
    uv sync --group dev --frozen

[doc("lint the code using ruff")]
lint:
    uv run ruff check

[doc("check static typing using mypy")]
typecheck:
    uv run mypy dj_bucket/ tests/

[doc("format the code using ruff")]
fmt:
    uv run ruff check --fix .
    uv run ruff format dj_bucket tests

[doc("run the unit tests suite")]
unittest test_suite=default_test_suite:
    uv run pytest -xv {{test_suite}}

[doc("run all code sanity check: linting typing and tests")]
test: lint typecheck unittest

[doc("bump a version of the package")]
release major_minor_patch:
    ./bin/tagging.sh {{major_minor_patch}}

[doc("Sync the lock file from pyproject.tom declaration without upgrading all.")]
update:
    #!/bin/bash
    uv sync --all-groups
    uv export --group dev --no-hashes > .gitlab/ci/requirements.txt

[doc("Update the dependencies with latest compatible version")]
upgrade: && update
    uv lock --upgrade
    uv export --group dev --no-hashes > .gitlab/ci/requirements.txt
