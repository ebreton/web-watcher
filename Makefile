#!make
# Default values, can be overridden either on the command line of make
# or in .env

.PHONY: init vars test coverage

vars:
	@echo 'Environment-related vars:'
	@echo '  DEFAULT_URL=${DEFAULT_URL}'
	@echo '  PYTHONPATH=${PYTHONPATH}'

start: clean check-env redis arq

redis:
	docker network create redis-network || true
	docker run -d \
		--name arq-redis \
		-p 6379:6379 \
		--network redis-network \
		-v $(PWD)/redis_data:/data \
		redis redis-server --appendonly yes

redis-cli:
	docker run -it --rm \
		--network redis-network \
		redis redis-cli -h arq-redis

arq:
	arq wwatch.arq.WorkerSettings

clean:
	docker stop arq-redis || true
	docker rm arq-redis || true

init:
ifeq ($(wildcard .env),)
	cp .env.sample .env
	echo PYTHONPATH=`pwd`/src >> .env
endif

lint: check-env
	flake8 src --max-line-length=120

test: lint
	pytest --cov=src tests

coverage: test
	coverage html
	open htmlcov/index.html

check-env:
ifeq ($(wildcard .env),)
	@echo "Please create your .env file first, from .env.sample or by running make venv"
	@exit 1
else
include .env
export
endif
