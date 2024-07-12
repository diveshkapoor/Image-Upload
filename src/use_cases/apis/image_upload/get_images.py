"""
Get Image endpoint lambda handler
"""
import logging
import json
import base64
from botocore.exceptions import ClientError
from src.core.services.images import ImageService
from src.core.constants.constants import IMAGES_REPO
from src.data_sources.dynamo_db.images_repo import ImageFilesRepo
from src.utils.cloud_storages.s3 import S3

logger = logging.getLogger()

s3_client = S3()
images = ImageService(s3_client)
images_repo = ImageFilesRepo(IMAGES_REPO)

def parse_s3_url(s3_url):
    """Parse an S3 URL into bucket name and key"""
    if s3_url.startswith("s3://"):
        s3_url = s3_url[5:]
    bucket_name, key = s3_url.split('/', 1)
    return bucket_name, key

def handler(event, context):
    """
    Lambda invocation method, fetches images from s3 bucket
    """
    logger.info('Starting process to fetch Images from s3')
    try:
        # Extract parameters from the API Gateway event
        s3_url = event['queryStringParameters']['s3_url']

        # Get the item from DynamoDB
        response = images_repo.fetch_image_details(s3_url)

        if 'Item' in response:
            # Parse the bucket name and key from the S3 URL
            bucket_name, key = parse_s3_url(s3_url)

            # Get the object from S3
            response = s3_client.get_object(bucket_name, key)
            content_type = response['ContentType']
            image_data = response['Body'].read()

            # Encode image data in base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            return {
                'statusCode': 200,
                'headers': {'Content-Type': content_type},
                'body': encoded_image,
                'isBase64Encoded': True
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'File not found'})
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request, missing query parameters'})
        }
    finally:
        logger.info('Process complete to fetch Images from s3')
