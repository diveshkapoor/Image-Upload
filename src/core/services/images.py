"""
Service class to enable image upload/download/deletion 
"""
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()

class ImageService():
    """
    Service class to download, upload images from s3 bucket, update db collection
    """

    def __init__(self, s3_client) -> None:
        self.s3_client = s3_client

    def upload_images(self, bucket_name, object_name, file_name):
        """uploads a file to S3"""
        try:
            self.s3_client.upload_file(self, bucket_name, object_name, file_name)
            print("File uploaded %s - ", file_name)
            # TODO: update db
        except ClientError as e:
            logger.error("Error occurred: -%s", e)


    def get_images(self, bucket_name, object_name):
        """Download a file from S3"""
        if file_name is None:
            file_name = object_name

        try:
            self.s3_client.download_file(self, bucket_name, object_name, file_name)
            print("File downloaded %s - ", file_name)
            # TODO: update db
        except ClientError as e:
            logger.error("Error occurred: -%s", e)

    def get_all_images(self, bucket_name, prefix=None):
        """List files in S3 bucket, optionally filtered by prefix"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                files = [item['Key'] for item in response['Contents']]
                return files
            else:
                return []
            # TODO: update db
        except ClientError as e:
            logger.error("Error occurred: -%s", e)

    def delete_image(self, bucket_name, file_name):
        """ Delete a file from S3 """
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            logger.info("File deleted %s - ", file_name)
            # TODO: update db
        except ClientError as e:
            logger.error("Error occurred: -%s", e)
