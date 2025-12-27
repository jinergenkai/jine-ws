.PHONY: help cpu gpu stop logs clean health test

help:
	@echo "Vintern OCR API - Commands"
	@echo ""
	@echo "  make cpu      - Run CPU version"
	@echo "  make gpu      - Run GPU version"
	@echo "  make stop     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make health   - Check health"
	@echo "  make test     - Test API"
	@echo "  make clean    - Clean everything"

cpu:
	@echo "Starting CPU version..."
	docker-compose --profile cpu up -d --build
	@echo "API running at http://localhost:11200"

gpu:
	@echo "Starting GPU version..."
	docker-compose --profile gpu up -d --build
	@echo "API running at http://localhost:11200"

stop:
	docker-compose down

logs:
	docker-compose logs -f

health:
	@curl -s http://localhost:11200/health | python -m json.tool || echo "Service not running"

test:
	@echo "Testing API..."
	@curl -X POST http://localhost:11200/extract \
		-F "file=@test-image.jpg" \
		-F "max_num=6" \
		-F "max_new_tokens=1024" | python -m json.tool

clean:
	docker-compose down -v
	docker rmi vintern-cpu vintern-gpu 2>/dev/null || true
	@echo "Cleaned!"
