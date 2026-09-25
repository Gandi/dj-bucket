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

[doc("Sync the lock file from pyproject.tom declaration without upgrading all.")]
update:
    uv sync --all-groups

[doc("Update the dependencies with latest compatible version")]
upgrade: && update
    uv lock --upgrade

release major_minor_patch: && changelog
    uv version --bump {{major_minor_patch}}

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv version --short --color=never)"
    git push
    git tag "v$(uv version --short --color=never)"
    git push origin "v$(uv version --short --color=never)"
