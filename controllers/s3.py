import boto3
import logging
from config import AWS_BUCKET, AWS_BASE

logger = logging.getLogger(__name__)
client = boto3.client("s3")


def upload_file_to_s3(file, filename):
    logger.info(f"FILENAME: {AWS_BASE + filename}")
    try:
        response = client.list_buckets()
        logger.info("Buckets")
        logger.info(response)
        client.upload_fileobj(file, AWS_BUCKET, AWS_BASE + filename)
        return True
    except Exception as e:
        logger.error("Error uploading to S3")
        logger.error(f"Error: {e}")
        return False
