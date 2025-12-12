UV := uv
PYTHON := python3
export PYTHONPATH := src
SECRETS_PATHS := src tests README.md pyproject.toml

.PHONY: setup bootstrap format format-check lint types security secrets check test deps-audit llm-live all

setup: ## Install project and dev dependencies via uv
	$(UV) sync

bootstrap: setup ## Alias for setup to match interface contract wording

format: ## Auto-format code
	$(UV) run python -m black src tests

format-check: ## Check formatting without modifying files
	$(UV) run python -m black --check src tests

lint: ## Ruff lint
	$(UV) run ruff check src tests

types: ## Type checks
	$(UV) run mypy src tests

security: ## Bandit security scan
	$(UV) run bandit -q -r src

secrets: ## Detect secrets, creating baseline if missing
	@if [ ! -f .secrets.baseline ]; then \
		echo "Creating .secrets.baseline"; \
		$(UV) run detect-secrets scan --all-files $(SECRETS_PATHS) > .secrets.baseline; \
	else \
		$(UV) run detect-secrets scan --all-files $(SECRETS_PATHS) > .secrets.scan.json; \
		$(PYTHON) -c "import json,sys; from pathlib import Path; data=json.loads(Path('.secrets.scan.json').read_text()); results=data.get('results') or {}; print('Potential secrets detected; see .secrets.scan.json') if results else None; sys.exit(1 if results else 0)" && mv .secrets.scan.json .secrets.baseline; \
	fi

check: format-check lint types security secrets ## Format check, lint, types, security, secrets

test: ## Run tests with coverage
	$(UV) run python -m pytest

deps-audit: ## Advisory dependency audit
	$(UV) run pip-audit

llm-live: ## Minimal live run to exercise LLM path
	$(UV) run python -m agentic_economy.cli llm-live --rounds 2 --n 3

all: check test ## Aggregate gate (add llm-live manually when needed)
