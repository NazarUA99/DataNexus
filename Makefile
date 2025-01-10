.PHONY: runBuildDocker runLocalDocker

SHELL := /bin/bash

runBuildLocalDocker:
	docker compose -f docker-compose.local.yml up -d --build

runLocalDocker:
	docker compose -f docker-compose.local.yml up -d

runBuildProdDocker:
	docker compose -f docker-compose.prod.yml up -d --build