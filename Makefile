# Scheduler0 Python client — release automation
#
# Usage:
#   make test                 Run the test suite
#   make build                Clean build + metadata check (artifacts in dist/)
#   make publish-test         Upload current dist/ to TestPyPI
#   make release VERSION=1.0.1 Bump version, build, publish to PyPI, tag, push
#
# Assumes PyPI credentials are configured (e.g. ~/.pypirc with a [pypi] token,
# or TWINE_USERNAME=__token__ / TWINE_PASSWORD env vars).

PY           := python3
VERSION_FILE := scheduler0/__init__.py
MAIN_BRANCH  := main

.PHONY: help install test build clean check publish-test publish release \
        guard-VERSION check-clean check-branch check-tag

help:
	@echo "make test                  - run the test suite"
	@echo "make build                 - clean build + twine check"
	@echo "make publish-test          - upload dist/ to TestPyPI"
	@echo "make publish               - build + upload current version to PyPI (no bump/tag)"
	@echo "make release VERSION=1.0.1 - bump, build, publish to PyPI, tag & push"

install:
	$(PY) -m pip install -e ".[dev]"
	$(PY) -m pip install --upgrade build twine

test:
	$(PY) -m pytest -q

clean:
	rm -rf dist build *.egg-info

build: clean
	$(PY) -m build
	$(PY) -m twine check dist/*

publish-test: build
	$(PY) -m twine upload --repository testpypi dist/*

publish: build
	$(PY) -m twine upload dist/*

release: guard-VERSION check-branch check-clean check-tag test
	@echo ">> Releasing scheduler0 v$(VERSION)"
	$(PY) -c "import re,pathlib; p=pathlib.Path('$(VERSION_FILE)'); s=p.read_text(); s2,n=re.subn(r'__version__ = \"[^\"]*\"', '__version__ = \"$(VERSION)\"', s); assert n==1, 'expected exactly one __version__ assignment in $(VERSION_FILE), found %d'%n; p.write_text(s2)"
	$(MAKE) build
	git add $(VERSION_FILE)
	git commit -m "Release v$(VERSION)"
	$(PY) -m twine upload dist/*
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin $(MAIN_BRANCH)
	git push origin v$(VERSION)
	@echo ">> Published scheduler0 $(VERSION) to PyPI and pushed tag v$(VERSION)"

# --- guards -----------------------------------------------------------------

guard-VERSION:
	@if [ -z "$(VERSION)" ]; then echo "ERROR: VERSION is required, e.g. make release VERSION=1.0.1"; exit 1; fi
	@echo "$(VERSION)" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+([abrc.+-].*)?$$' || { echo "ERROR: VERSION '$(VERSION)' is not a valid version (expected x.y.z)"; exit 1; }

check-branch:
	@if [ "$$(git branch --show-current)" != "$(MAIN_BRANCH)" ]; then echo "ERROR: not on '$(MAIN_BRANCH)' branch"; exit 1; fi

check-clean:
	@if [ -n "$$(git status --porcelain)" ]; then echo "ERROR: working tree is dirty; commit or stash first"; exit 1; fi

check-tag:
	@if git rev-parse -q --verify "refs/tags/v$(VERSION)" >/dev/null; then echo "ERROR: tag v$(VERSION) already exists"; exit 1; fi
