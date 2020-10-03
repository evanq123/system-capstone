# Starts bash in docker container
.PHONY: run
run:
	docker build \
		-t meks/system-capstone:system-project \
		-f Dockerfile.app .
	docker run -it --rm --privileged  \
		--name app meks/system-capstone:system-project \
		bash

# runs benchmarking scripts on app
.PHONY: benchmark
benchmark:
	docker build \
		-t meks/system-capstone:system-project \
		-f Dockerfile.app .
	docker run -it --rm --privileged  \
		--name app meks/system-capstone:system-project \
		./scripts/benchmark.sh
	
# runs unit tests
.PHONY: test
test:
	docker build \
		-t meks/system-capstone:system-project \
		-f Dockerfile.app .
	docker run -it --rm --privileged  \
		--name app meks/system-capstone:system-project \
		./scripts/test.sh

# Sets up REDIS database as Docker container
.PHONY: redis
redis:
	
# Sets up SQL database as Docker container
.PHONY: sql
sql:
	