.EXPORT_ALL_VARIABLES:

MODEL=randomforest
VERSION=v1.0
IMAGE_TAG=${MODEL}-${VERSION}
PORT=8080
ENDPOINT=http://localhost:${PORT}/v1/models/${MODEL}:predict
CONTAINER_NAME=inference-service

setup:
	pip install -r /requirements.txt

train:
	PYTHONPATH=. python bin/train.py

build:
	docker build -f Dockerfile -t ${IMAGE_TAG} .

run: build
	docker rm ${CONTAINER_NAME} || echo "Running container"
	docker run --name ${CONTAINER_NAME} -it -p 8080:8080 ${IMAGE_TAG}

request:
	curl -X POST ${ENDPOINT} -H "Content-Type: application/json" -d @input.json > predictions.json