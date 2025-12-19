UV := uv
PYTHON := python3
export PYTHONPATH := src
SECRETS_PATHS := src tests README.md pyproject.toml

.PHONY: setup bootstrap format format-check lint types security secrets check test deps-audit llm-live all
.PHONY: results-core results-all
.PHONY: figures-core report
.PHONY: results-pages

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
		files=$$(git ls-files $(SECRETS_PATHS)); \
		if [ -z "$$files" ]; then \
			echo "No files matched for secret scanning"; \
			exit 0; \
		fi; \
		$(UV) run detect-secrets-hook --baseline .secrets.baseline $$files; \
	fi

check: format-check lint types security secrets ## Format check, lint, types, security, secrets

test: ## Run tests with coverage
	$(UV) run python -m pytest

deps-audit: ## Advisory dependency audit
	$(UV) run pip-audit

llm-live: ## Minimal live run to exercise LLM path
	$(UV) run python -m agentic_economy.cli llm-live --rounds 2 --n 3 --model gpt-5-mini

results-core: ## Generate full + aggregated tables for runs_core
	$(UV) run python -m agentic_economy.analysis --pattern 'runs_core/*.json' --out-csv results/runs_core_full.csv --out-md results/runs_core_full.md --out-aggregate-csv results/runs_core_aggregate.csv --out-aggregate-md results/runs_core_aggregate.md

results-all: ## Generate full + aggregated tables for all local runs*
	$(UV) run python -m agentic_economy.analysis --pattern 'runs*/*.json' --out-csv results/all_runs_full.csv --out-md results/all_runs_full.md --out-aggregate-csv results/all_runs_aggregate.csv --out-aggregate-md results/all_runs_aggregate.md

figures-core: ## Generate blog/paper-friendly figures and LaTeX for core sweep
	$(UV) run python -m agentic_economy.reporting --core-aggregate results/runs_core_aggregate.csv --out-dir results/figures --paper-dir results/paper

report: figures-core ## Alias for figures-core

results-pages: ## Generate consolidated results pages (all + showcase)
	$(UV) run python -m agentic_economy.results_pages

all: check test ## Aggregate gate (add llm-live manually when needed)
