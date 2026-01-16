
import asyncio
from app.modules.utils.object_service import ObjectService

async def main():
    service = ObjectService()
    # No need to actually connect for presigned URL generation as it uses boto3 client which is sync and init in __init__
    # but let's follow pattern if needed. Actually _encure_connected is for http client.
    # _get_s3_client is called in __init__.
    
    url = service.get_url("test-key")
    print(f"Generated URL:\n{url}")
    
    if "X-Amz-Signature" in url:
        print("SUCCESS: URL uses V4 Signature")
    else:
        print("FAILURE: URL uses Legacy Signature")

if __name__ == "__main__":
    asyncio.run(main())
