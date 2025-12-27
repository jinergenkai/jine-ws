.PHONY: help build-cpu build-gpu up-cpu up-gpu down logs health clean test

help:
	@echo "Vintern OCR API - Docker Commands"
	@echo ""
	@echo "CPU Version:"
	@echo "  make build-cpu    - Build CPU image"
	@echo "  make up-cpu       - Start CPU service"
	@echo "  make down-cpu     - Stop CPU service"
	@echo ""
	@echo "GPU Version:"
	@echo "  make build-gpu    - Build GPU image"
	@echo "  make up-gpu       - Start GPU service"
	@echo "  make down-gpu     - Stop GPU service"
	@echo ""
	@echo "General:"
	@echo "  make logs         - View logs"
	@echo "  make health       - Check health status"
	@echo "  make clean        - Remove all containers and images"
	@echo "  make test         - Test API with sample image"

# CPU Commands
build-cpu:
	docker-compose --profile cpu build

up-cpu:
	docker-compose --profile cpu up -d
	@echo "API running at http://localhost:11200"
	@echo "Docs at http://localhost:11200/docs"

down-cpu:
	docker-compose --profile cpu down

# GPU Commands
build-gpu:
	docker-compose --profile gpu build

up-gpu:
	docker-compose --profile gpu up -d
	@echo "API running at http://localhost:11200"
	@echo "Docs at http://localhost:11200/docs"

down-gpu:
	docker-compose --profile gpu down

# General Commands
logs:
	docker-compose logs -f

health:
	@echo "Checking service health..."
	@curl -s http://localhost:11200/health | python -m json.tool || echo "Service not running"

clean:
	docker-compose --profile cpu down -v
	docker-compose --profile gpu down -v
	docker system prune -f

test:
	@echo "Testing API (requires service to be running)..."
	@curl -X POST http://localhost:11200/extract \
		-F "file=@test-image.jpg" \
		-F "max_num=6" \
		-F "max_new_tokens=1024" | python -m json.tool
