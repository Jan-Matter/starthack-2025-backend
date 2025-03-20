#!/bin/bash

echo "Setting environment variables and secrets for branch $RUN_ID"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

case $CURRENT_BRANCH in
  release)
    env="test"
    export TES_CPUS=1
    export TES_REPLICAS=1
    export TES_MIN_REPLICAS=1
    export TES_MAX_REPLICAS=1
    export TES_AWS_SECRET_NAME="aws-secret-test"
    export TES_CLUSTER_ISSUER="letsencrypt-test"
    export TES_DOMAIN="helvetai-test.dataplumbers.ch"
    ;;
  master)
    env="prod"
    export TES_CPUS=1
    export TES_REPLICAS=2
    export TES_MIN_REPLICAS=2
    export TES_MAX_REPLICAS=10
    export TES_AZURE_KEYVAULT_SECRET_NAME="aws-secret-test"
    export TES_CLUSTER_ISSUER="letsencrypt-prod"
    export TES_DOMAIN="helvetai.dataplumbers.ch"
    ;;
  *) echo 'Unknown branch for K8s deployment' >&2
    ;;
esac

export DOCKER_HOST=tcp://localhost:2375
export ENVIRONMENT_NAME=$env
echo "$ENVIRONMENT_NAME environment set"

export TES_IMAGE="046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-$env/api"
export TES_IMAGE_TAG="$TES_IMAGE:$(echo "$RUN_ID" | tr -d '{}')"