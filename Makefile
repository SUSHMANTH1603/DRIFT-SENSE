.PHONY: help install test lint generate train benchmark clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -e ".[dev]"
	pip install -r requirements.txt

test:  ## Run all tests
	pytest tests/ -v --tb=short

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=classical --cov=generator --cov=models --cov=evaluation --cov=inference --cov-report=html

lint:  ## Lint and format check
	ruff check .
	black --check .
	mypy classical/ generator/ models/ evaluation/ inference/

format:  ## Auto-format code
	black .
	ruff check --fix .

generate:  ## Generate synthetic dataset (1000 DRAM + 1000 FinFET pairs)
	python -m generator.generate_dataset --style DRAM --count 1000 --output data/generated/train
	python -m generator.generate_dataset --style FinFET --count 1000 --output data/generated/train
	python -m generator.generate_dataset --style DRAM --count 200 --output data/generated/val
	python -m generator.generate_dataset --style FinFET --count 200 --output data/generated/val
	python -m generator.generate_dataset --style DRAM --count 200 --output data/generated/test
	python -m generator.generate_dataset --style FinFET --count 200 --output data/generated/test

train:  ## Train Siamese fallback model (Phase 4)
	python -m training.train --config configs/siamese.yaml

benchmark:  ## Run full benchmark suite
	python -m evaluation.benchmark --config configs/inference.yaml --data data/generated/test

infer:  ## Run inference (usage: make infer REF=ref.png SEARCH=search.png)
	python -m inference.infer $(REF) $(SEARCH) --config configs/inference.yaml

clean:  ## Clean generated artifacts
	rm -rf data/generated/ results/ checkpoints/ __pycache__ .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
