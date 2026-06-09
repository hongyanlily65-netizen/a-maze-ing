VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
HAS_BEEN_INSTALLED = $(VENV)/.has_been_installed

run: $(VENV)
	$(PYTHON) a_maze_ing.py config.txt

$(VENV):
	python3 -m venv $(VENV)

install: $(HAS_BEEN_INSTALLED)

$(HAS_BEEN_INSTALLED): $(VENV)
	$(PIP) install -r requirements.txt
	@touch $(HAS_BEEN_INSTALLED)
	@echo "Dependencies installed."

debug: $(VENV)
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint: install
	$(VENV)/bin/flake8 a_maze_ing.py src
	$(VENV)/bin/mypy a_maze_ing.py src \
		--explicit-package-bases \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

build: install
	$(PYTHON) -m build --sdist --outdir .

clean:
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "build" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

.PHONY: run install debug lint build clean
