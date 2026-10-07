PY := uv run python

.PHONY: setup data train evaluate api dashboard test lint check docker-up docker-down dev gen-types e2e demo deploy verify-deploy ping

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
	uv run pytest -q

lint:
	uv run ruff check src tests datagen scripts api dashboard
	uv run pyright

check:
	uv run ruff check src tests datagen scripts api dashboard
	uv run pyright
	uv run pytest -q
	$(MAKE) gen-types
	git diff --exit-code -- web/src/api/openapi.json web/src/api/schema.d.ts
	cd web && npx tsc -b --noEmit
	cd web && npx oxlint src e2e
	cd web && npx vite build

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

demo:
	@echo demo not built yet

deploy:
	npx -y vercel --prod

verify-deploy:
	uv run python scripts/verify_deploy.py $(URL) $(FLAGS)

ping:
	@U=$$(grep -E '^SUPABASE_URL=' .env 2>/dev/null | cut -d= -f2- | tr -d '\r'); \
	K=$$(grep -E '^SUPABASE_SERVICE_ROLE_KEY=' .env 2>/dev/null | cut -d= -f2- | tr -d '\r'); \
	if [ -z "$$U" ] || [ -z "$$K" ]; then echo "PAUSED (missing .env credentials)"; exit 1; fi; \
	C=$$(curl -s -o /dev/null -w "%{http_code}" -H "apikey: $$K" "$$U/rest/v1/"); \
	if [ "$$C" = "200" ]; then echo "OK ($$U)"; exit 0; else echo "PAUSED (HTTP $$C)"; exit 1; fi
