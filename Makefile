# ============================================================
#  Makefile — development shortcuts
#  Usage: make <target>
# ============================================================
 
COMPOSE_PROD = docker compose -f docker-compose.yml
COMPOSE_DEV  = docker compose -f docker-compose.yml -f docker-compose.dev.yml

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "  Cinema Reservation System"
	@echo ""
	@echo "  Dev"
	@echo "    make dev            Start all services (attached, shows logs)"
	@echo "    make dev-build      Start all services and rebuild images"
	@echo "    make dev-down       Stop all services"
	@echo "    make dev-clean      Stop all services and wipe volumes"
	@echo ""
	@echo "  Production (simulation)"
	@echo "    make prod-build     Build production images"
	@echo "    make prod-up        Start in production mode (detached)"
	@echo "    make prod-down      Stop production services"
	@echo ""
 
# ── Dev lifecycle ────────────────────────────────────────────
 
dev:
	$(COMPOSE_DEV) up
 
dev-build:
	$(COMPOSE_DEV) up --build
 
dev-down:
	$(COMPOSE_DEV) down
 
dev-clean:
	$(COMPOSE_DEV) down -v --remove-orphans

dev-mobile:
	cd mobile/mobile_main_app; open -a Simulator; sleep 5; flutter run

# ── Production simulation (no dev overrides) ─────────────────
 
prod-build:
	$(COMPOSE_PROD) build
 
prod-up:
	$(COMPOSE_PROD) up -d
 
prod-down:
	$(COMPOSE_PROD) down
