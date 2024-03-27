.POSIX:
.SUFFIXES:

all: fmt lint

fmt:
	ruff format

lint:
	ruff check

mypy:
	mypy .

# run `make pre-commit` once to install the hook.
pre-commit: .git/hooks/pre-commit fmt lint mypy
	git diff --exit-code

.git/hooks/pre-commit:
	echo "make pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
