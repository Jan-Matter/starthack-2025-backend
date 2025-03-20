#!/bin/bash


case $GITHUB_REF_NAME in
  release)
    env="test"
    ;;
  main)
    env="prod"
    ;;
  *) echo "This image won't be pushed" >&2
    exit 0;
esac

export TES_IMAGE="046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-$env/api:$GITHUB_SHA"

docker build -t "$TES_IMAGE" . 


docker push $TES_IMAGE