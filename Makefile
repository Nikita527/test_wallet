# Старт базы данных
start-db:
	docker-compose -f infra/dev/docker-compose.dev.yaml up -d postgres

# Остановка базы данных
stop-db:
	docker-compose -f infra/dev/docker-compose.dev.yaml down

run:
	uvicorn app.main:app --reload

pytest:
	pytest

start:
	docker-compose -f infra/dev/docker-compose.dev.yaml up -d --build

stop:
	docker-compose -f infra/dev/docker-compose.dev.yaml down --volumes

test:
	pytest app/tests/
