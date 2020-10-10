test: build
	docker run igit_test


build: Dockerfile
	docker build --rm -t igit_test .
