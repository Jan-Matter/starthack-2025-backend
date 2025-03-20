
git clone https://github.com/Jan-Matter/starthack-2025-deployment.git
cd starthack-2025-deployment
git checkout $CURRENT_BRANCH

cd helmcharts/starthack-backend-chart
sed -i "s/^.*image:.*$/image: TES_IMAGE/" values.yaml
git add values.yaml
git commit -m "Update image tag for deployment $RUN_ID"
git push origin $CURRENT_BRANCH

cd ../../..
