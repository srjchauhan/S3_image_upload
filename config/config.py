import os


class S3Config:
    aws_access_key_id = os.environ.get("AWS_ACCESS_ID")
    aws_secret_access_key = os.environ.get("AWS_ACCESS_KEY")
    region_name = os.environ.get("REGION_NAME")
    bucket_name = os.environ.get("BUCKET_NAME")
    bucket_dir = os.environ.get("BUCKET_DIR")


class PathConfig:
    temp_path = os.environ.get('TEMP_DIR')
