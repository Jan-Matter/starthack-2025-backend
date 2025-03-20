
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

git config --global user.email "jan.matter@outlook.com"
git config --global user.name "Jan Matter"

git clone https://github.com/Jan-Matter/starthack-2025-deployment.git
cd starthack-2025-deployment
git checkout $GITHUB_REF_NAME

echo "Updating image tag for deployment $GITHUB_SHA"
echo "Environment: $env"

cd helmcharts/starthack-backend-chart
sed -i "s/^.*image:.*$/image: 046776365295.dkr.ecr.eu-central-1.amazonaws.com\/starthack-$env\/api:$GITHUB_SHA\/" values.yaml
git add values.yaml
git commit -m "Update image tag for deployment $GITHUB_SHA"
git push origin $GITHUB_REF_NAME

cd ../../..
