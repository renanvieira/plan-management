start-docker:
	docker-compose up -d

stop-docker:
	docker-compose rm -sf

run-tests:
	nosetests tests/workout_tests/integration --with-coverage  --cover-package=virtuagym_api -s