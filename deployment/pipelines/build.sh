#!/bin/bash

export TES_IMAGE="046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-$env/api:$RUN_ID"

docker build -t "$TES_IMAGE" . 

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


docker push $TES_IMAGE