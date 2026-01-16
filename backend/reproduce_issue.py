
import boto3
from botocore.config import Config

def check_signature_version():
    # Simulate the settings and client creation
    endpoint = "https://example.storage.supabase.co/storage/v1/s3"
    region = "us-east-1"
    access_key = "test"
    secret_key = "test"
    
    # Current implementation in ObjectService (default)
    s3_default = boto3.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    
    url_default = s3_default.generate_presigned_url(
        "put_object",
        Params={"Bucket": "documents", "Key": "test.txt", "ContentType": "text/plain"},
        ExpiresIn=3600
    )
    
    print(f"Default Client URL:\n{url_default}\n")

    if "Signature=" in url_default and "X-Amz-Signature" not in url_default:
        print("-> Uses v2/legacy signature (Problematic)")
    else:
        print("-> Uses v4 signature (Likely Correct)")

    # Proposed Fix: Enforce v4
    s3_v4 = boto3.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4')
    )
    
    url_v4 = s3_v4.generate_presigned_url(
        "put_object",
        Params={"Bucket": "documents", "Key": "test.txt", "ContentType": "text/plain"},
        ExpiresIn=3600
    )
    
    print(f"\nv4 Client URL:\n{url_v4}\n")

if __name__ == "__main__":
    check_signature_version()
