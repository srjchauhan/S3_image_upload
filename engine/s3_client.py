import os.path

import boto3
from config import S3Config, PathConfig
from botocore.exceptions import ClientError


class s3_client:
    def __init__(self) -> None:
        self._temp_path = PathConfig.temp_path
        self.client = boto3.client('s3', aws_access_key_id=S3Config.aws_access_key_id,
                                   aws_secret_access_key=S3Config.aws_secret_access_key,
                                   region_name=S3Config.region_name)

    def check_file_exist(self, filename):
        resp = self.client.list_objects_v2(Bucket=S3Config.bucket_name,
                                           Prefix=os.path.join(S3Config.bucket_dir, filename))
        if resp['KeyCount'] > 0:
            return True
        else:
            return False

    def upload_image(self, name):
        local_image_path = os.path.join(self._temp_path, name)
        tmp_objectName = os.path.join(S3Config.bucket_dir, name) if len(S3Config.bucket_dir) > 0 else os.path.basename(
            name)
        try:
            response = self.client.upload_file(local_image_path, S3Config.bucket_name, tmp_objectName)
        except ClientError as e:
            return False, str(e)
        return True, response

    def list_images(self):
        try:
            obj = self.client.list_objects_v2(Bucket=S3Config.bucket_name, Prefix=S3Config.bucket_dir)
            return True, [i['Key'] for i in obj['Contents']]
        except ClientError as e:
            return False, str(e)


if __name__ == "__main__":
    s3 = s3_client()
    obj = s3.list_images()
    print(obj)
