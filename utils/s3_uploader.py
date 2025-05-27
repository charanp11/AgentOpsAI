import boto3
import uuid
import os
from botocore.exceptions import NoCredentialsError

def upload_zip_to_s3(zip_data, bucket_name=None, expiration=300):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1"  
        )

        if not bucket_name:
            bucket_name = os.getenv("S3_BUCKET_NAME")

        file_key = f"agentops_exports/{uuid.uuid4()}.zip"
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=zip_data.getvalue())

        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_key},
            ExpiresIn=expiration
        )
        return presigned_url

    except NoCredentialsError:
        return None
