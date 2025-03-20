# This repo implements the Backend for the Start Hack 2025 Project


### Setup of Repo
- Add the env variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY of the AWS service account to your computer. On linux one can add 
- `export AWS_ACCESS_KEY_ID=<your_access_key_id>`
- `export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>`
to the ~/.bashrc to set env variables for example to load them whenever a shell is started.
Run
- `source ~/.bashrc` to init env variables afterwards
- activate conda env from environment.yaml `conda env create -f environment.yml`
- install repository `python -m pip install -e .`

### Build Docker Image and Push to Docker Repository
- `docker build -t 046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-test/api:<version> .`
- if not already install aws cli tool
- `aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 046776365295.dkr.ecr.eu-central-1.amazonaws.com`
- `docker push 046776365295.dkr.ecr.eu-central-1.amazonaws.com/starthack-test/api:<version>`
