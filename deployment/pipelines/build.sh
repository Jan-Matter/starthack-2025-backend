#!/bin/bash

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

export TES_IMAGE="046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-$env/api:$RUN_ID"

docker push $TES_IMAGE