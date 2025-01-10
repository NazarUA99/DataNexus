.PHONY: runLocal runBuildDocker runDocker

SHELL := /bin/bash

applyMigration:
	source .env.local && \
	alembic upgrade head

createMigration:
	source .env.local && \
	alembic revision --autogenerate -m "new migration"

downgradeMigration:
	source .env.local && \
	alembic downgrade -1

runLocal:
	source .env.local && \
	uvicorn app.server:app --host 0.0.0.0 --reload --port 8009 --timeout-keep-alive 600 --log-config ./config.local.ini --log-level debug