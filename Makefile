run-containers:
	docker-compose up -d

makemigrations:
	docker-compose run --rm api python manage.py makemigrations

migrate: makemigrations
	docker-compose run --rm api python manage.py migrate

shell:
	docker-compose run --rm api python manage.py shell

shell-plus:
	docker-compose run --rm api python manage.py shell_plus

test:
	docker-compose run --rm api python manage.py test

test-coverage:
	docker-compose run --rm api coverage run --source='.' manage.py test

test-report: test-coverage
	docker-compose run --rm api coverage report

test-html-report: test-coverage
	docker-compose run --rm api coverage html
