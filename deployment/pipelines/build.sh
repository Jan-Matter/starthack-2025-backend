#!/bin/bash

sudo snap install aws-cli --classic
echo aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin "$DOCKER_REGISTRY"

docker build -t "$TES_IMAGE_TAG" . 

case $CURRENT_BRANCH in
  release)
    env="test"
    ;;
  master)
    env="prod"
    ;;
  *) echo "This image won't be pushed" >&2
    exit 0;
esac

docker tag "$TES_IMAGE_TAG" "$TES_IMAGE:$env"
docker push "$TES_IMAGE_TAG"
docker push "$TES_IMAGE:$env"