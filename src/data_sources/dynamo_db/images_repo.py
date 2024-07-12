"""
Image Metadata Repo file to fetch image info from db collection
"""
import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

logger = logging.getLogger()

class ImageFilesRepo:
    """
    Image Metadata Repo class to fetch image details from db collection
    """
    def __init__(self, table_name):
        self.dynamodb = boto3.resource(
            'dynamodb',
        )
        self.table = self.dynamodb.Table(table_name)

    def fetch_image_details(self, file_name):
        """Get details for given image from collection"""
        try:
            response = self.table.get_item(Key={
                'file_name': file_name,})
            return response.get('Item')
        except NoCredentialsError:
            logging.error("Credentials not available.")
        except ClientError as e:
            logger.error("Error occurred: -%s", e)
            return None

    def update_image_details(self, file_name, update_expression, expression_attribute_values):
        """Update details in collection"""
        try:
            response = self.table.update_item(
                Key={ 'file_name': file_name,},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            return response
        except NoCredentialsError:
            logging.error("Credentials not available.")
        except ClientError as e:
            logger.error("Error occurred: -%s", e)
            return None

    def delete_image_details(self, file_name):
        """Delete image details from collection"""
        try:
            response = self.table.delete_item(Key={
                'file_name': file_name,})
            return response
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            logger.error("Error occurred: -%s", e)
            return None
