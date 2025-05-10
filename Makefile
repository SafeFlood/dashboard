build:
	docker-compose build
	
run:
	docker-compose up -d --build --force-recreate

stop:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec safeflood /bin/bash