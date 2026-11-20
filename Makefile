PYTHON ?= python3

.PHONY: help validate catalog check install uninstall

help:
	@echo "make validate   - validate skills"
	@echo "make catalog    - regenerate catalog.json and README table"
	@echo "make check      - validate and verify generated files are current"
	@echo "make install    - link skills into opencode and Claude Code"
	@echo "make uninstall  - remove links owned by this repository"

validate:
	$(PYTHON) scripts/validate.py

catalog:
	$(PYTHON) scripts/build_catalog.py

check:
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/build_catalog.py --check

install:
	./scripts/install.sh --target all

uninstall:
	./scripts/install.sh --target all --uninstall
