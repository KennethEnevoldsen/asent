install:
	pip install -e ".[da, all, docs, tests]"

lint:
	pre-commit run --all-files

test:
	pytest -v

static-type-check:
	pyright src/

pr:
	make lint
	make static-type-check
	make test