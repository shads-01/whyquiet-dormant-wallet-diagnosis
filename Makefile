PY := uv run python

.PHONY: setup data train evaluate api dashboard test lint check docker-up docker-down dev gen-types e2e deploy verify-deploy

setup:
	uv sync --all-extras --dev

data:
	$(PY) scripts/generate_data.py

train:
	$(PY) scripts/train_models.py

evaluate:
	$(PY) scripts/evaluate_all.py

api:
	uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8008 --reload

dashboard:
	uv run streamlit run dashboard/app.py --server.port 8501

test:
	uv run pytest -v --cov=src --cov-report=term-missing

lint:
	uv run ruff check src tests config scripts
	uv run pyright

check: lint test
	@echo "All static checks and test suites passed successfully."

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

dev:
	uv run $(if $(wildcard .env),--env-file .env) uvicorn src.api.main:app --port 8008 &
	cd web && npm run dev

gen-types:
	$(PY) scripts/export_openapi.py
	cd web && npx -y openapi-typescript src/api/openapi.json -o src/api/schema.d.ts

e2e:
	cd web && npx playwright test

deploy:
	npx -y vercel --prod

verify-deploy:
	uv run python scripts/verify_deploy.py $(URL) $(FLAGS)
