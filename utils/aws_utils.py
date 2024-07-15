# utils/aws_utils.py
import logging

import boto3
from botocore.exceptions import ClientError


def upload_file(file_obj, bucket, object_name):
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_fileobj(file_obj, bucket, object_name, ExtraArgs={"ContentType": "application/pdf"})
    except ClientError as e:
        logging.error(e)
        return False
    return True
