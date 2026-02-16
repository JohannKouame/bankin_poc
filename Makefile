RUN_PYTHON=docker compose run --rm python

.PHONY: install
install:
	@test -f .env || (echo "Generating .env file using .env.dist" && cp .env.dist .env) || true
	docker compose build --no-cache

.PHONY: sh
sh:
	${RUN_PYTHON} sh

.PHONY: download_dataset
download_dataset:
	docker compose run --rm -e PYTHONPATH=/app python python src/command/download_dataset.py --url=$(url)

.PHONY: build_features
build_features:
	docker compose run --rm -e PYTHONPATH=/app python python src/command/build_features.py

.PHONY: run_streamlit
run_streamlit:
	docker compose run --rm -e PYTHONPATH=/app python python src/command/run_streamlit.py
