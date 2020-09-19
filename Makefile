test: build
	docker run gitsy_stage


build: Dockerfile
	docker build --rm -t gitsy_stage .
