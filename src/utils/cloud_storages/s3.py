"""
S3 Storage Implementation file
"""
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()

class S3():
    """
    Utility class to provide access to AWS S3
    """

    def __init__(self):
        logger.debug('Loading S3 Module')
        self.s3_client = boto3.client('s3')

    def get_object(self, object_key, s3_bucket):
        """
        Gets object from s3
        """
        bucket = self.s3_client.get_object(Bucket=s3_bucket,
                                           key=object_key)["Body"].read()
        logger.debug('Bucket output data - %s', bucket)
        return bucket

    def download_file(self, bucket_name, object_name, file_name):
        """
        Download file from s3
        """
        self.s3_client.download_file(bucket_name, object_name, file_name)

    def upload_file(self, file_name, bucket, object_name=None):
        """
        Uploads a file to s3 bucket
        """

        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as err:
            logging.error(err)
            return False
        return True
