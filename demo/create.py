import argparse
import asyncio
from aiobotocore.session import get_session

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("s3_url", help="URL for S3")
    parser.add_argument("s3_id", help="ID for S3")
    parser.add_argument("s3_accesskey", help="AccessKey for S3")
    parser.add_argument("bucket", help="Bucket")
    parser.add_argument("path", help="path")
    parser.add_argument("start", help="start", type=int)
    parser.add_argument("count", help="count", type=int)
    args = parser.parse_args()

    session = get_session()
    async with session.create_client('s3', endpoint_url=args.s3_url, use_ssl=False,
                                     aws_secret_access_key=args.s3_accesskey,
                                     aws_access_key_id=args.s3_id) as client:
        # upload object to amazon s3
        for calc in range(0, args.count):
            data = str(args.start + calc).encode()
            key = f'{args.path}/{calc}.txt'
            resp = await client.put_object(Bucket=args.bucket,
                                           Key=key,
                                           Body=data,
                                           ContentType='text/plain')
            print(resp)

if __name__ == '__main__':
    asyncio.run(main())
