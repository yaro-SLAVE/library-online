dev: create-backend-dirs
	cp -n .env.example .env || true
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

restart:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

logs:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

clear:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes --rmi all

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

up-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d


restart-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down


logs-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

clear-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down --volumes --rmi all

create-backend-dirs:
	mkdir -p backend/media backend/staticfiles
