import boto3
import logging
from config import AWS_BUCKET, AWS_BASE
import random
import string

logger = logging.getLogger(__name__)
client = boto3.client("s3")


def upload_file_to_s3(file, filename):
    logger.info(f"FILENAME: {AWS_BASE + filename}")
    letters = string.ascii_lowercase
    file_prepend = "".join(random.choice(letters) for i in range(10))
    try:
        final_filename = AWS_BASE + file_prepend + filename
        client.upload_fileobj(file, AWS_BUCKET, final_filename)
        return final_filename
    except Exception as e:
        logger.error("Error uploading to S3")
        logger.error(f"Error: {e}")
        return False
