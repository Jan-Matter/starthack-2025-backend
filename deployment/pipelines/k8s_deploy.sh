
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

git clone https://github.com/Jan-Matter/starthack-2025-deployment.git
cd starthack-2025-deployment
git checkout $CURRENT_BRANCH

cd helmcharts/starthack-backend-chart
sed -i "s/^.*image:.*$/image: $TES_IMAGE/" values.yaml
git add values.yaml
git commit -m "Update image tag for deployment $RUN_ID"
git push origin $CURRENT_BRANCH

cd ../../..
