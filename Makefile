.PHONY:
	build
	dev
	clean
	fresh


# Build waveapp
build:
	docker-compose build

dev:
	docker-compose up

clean:
	docker-compose rm -f

fresh: build dev
