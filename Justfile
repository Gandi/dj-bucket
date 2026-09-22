package := 'dj_bucket'

install:
    uv sync --group dev

lint:
    uv run ruff check .

fmt:
    uv run ruff check --fix .
    uv run ruff format dj_bucket

release major_minor_patch: && changelog
    uv version --bump {{major_minor_patch}}

changelog:
    uv run python scripts/write_changelog.py
    tail -n +4 CHANGES.rst >> CHANGES.rst.new
    rm CHANGES.rst
    mv CHANGES.rst.new CHANGES.rst
    $EDITOR CHANGES.rst

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git push
    git tag "v$(uv run scripts/get_version.py)"
    git push origin "v$(uv run scripts/get_version.py)"
