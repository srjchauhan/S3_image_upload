import os


class S3Config:
    aws_access_key_id = os.environ.get("AWS_ACCESS_ID")
    aws_secret_access_key = os.environ.get("AWS_ACCESS_KEY")
    region_name = os.environ.get("REGION_NAME")
    bucket_name = os.environ.get("BUCKET_NAME")
    bucket_dir = os.environ.get("BUCKET_DIR")
    isLocal = False
    endpoint_url = ''


class PathConfig:
    temp_path = os.environ.get('TEMP_DIR')


class DynamodbConfig:
    table_name = 's3_image_data'
    islocal = False
    endpoint_url = ''
