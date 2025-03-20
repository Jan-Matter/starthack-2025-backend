from pathlib import Path
import boto3
import os

class S3FileStore:

    def __init__(self):
        """
        This method should initialize the filestore client with the given config.
        - config: A dictionary containing the necessary configuration to initialize the filestore client.
            - aws_access_key_id: The access key for the AWS account.
            - aws_secret_access_key: The secret access key for the AWS account.
        """
        boto3.setup_default_session()
        self._s3_client = boto3.client('s3')

    def save(self, localpath: Path, bucket_name: str, file_name: str, **kwargs):
        self._s3_client.upload_file(localpath, bucket_name, file_name)


    def load(self, localpath: Path, bucket_name: str, file_name: str, **kwargs):
        if os.path.exists(localpath):
            return
        self._s3_client.download_file(bucket_name, file_name, localpath)
            
    
    def load_folder(self, localpath: Path, bucket_name: str, folder_name: str, **kwargs):
        files = self._s3_client.list_objects(Bucket=bucket_name, Prefix=folder_name)
        os.makedirs(localpath, exist_ok=True)
        for file in files['Contents']:
            file_key = file['Key']
            local_file_path = localpath / file_key.split('/')[-1]
            self._s3_client.download_file(bucket_name, file_key, local_file_path)


    def save_folder(self, localpath: Path, bucket_name: str, folder_name: str, **kwargs):
        for file in localpath.iterdir():
            self._s3_client.upload_file(file, bucket_name, f"{folder_name}/{file.name}")



if __name__ == '__main__':

    from shared.constants import S3_BUCKET_NAME

    ENV = os.getenv('ENV', 'test')

    s3_filestore = S3FileStore()
    s3_filestore.save(Path('./test.txt'), S3_BUCKET_NAME, f'{ENV}/test.txt')

