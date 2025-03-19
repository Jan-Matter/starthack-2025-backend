
import boto3
from botocore.exceptions import ClientError
import json


class AWSSecretClient:


    def get_secret(self, secret_name: str, secret_key: str, region_name: str) -> str:

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
        secret_string_parsed = json.loads(get_secret_value_response['SecretString'])
        secret = secret_string_parsed[secret_key]
        return secret


if __name__ == '__main__':
    secret_client = AWSSecretClient()
    secret_name = 'starthack_2025_test_postgres_connstr'
    secret_key = 'starthack_2025_test_postgres_connstr'
    region_name = 'eu-central-1'
    secret_client.get_secret(secret_name, secret_key, region_name)
