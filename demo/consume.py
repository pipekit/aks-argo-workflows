import argparse
import asyncio
import json
import nats
import time
from aiobotocore.session import get_session
from nats.errors import TimeoutError

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nats_address", help="Address of NATS")
    parser.add_argument("stream", help="Stream")
    parser.add_argument("s3_url", help="URL for S3")
    parser.add_argument("s3_id", help="ID for S3")
    parser.add_argument("s3_accesskey", help="AccessKey for S3")
    parser.add_argument("bucket", help="Bucket")
    args = parser.parse_args()
    nc = await nats.connect(args.nats_address)

    # Create JetStream context.
    js = nc.jetstream()
    # Access jetstream manager
    jsm = nc.jsm()

    existing_consumers = dict()
    session = get_session()
    async with session.create_client('s3', endpoint_url=args.s3_url, use_ssl=False,
                                     aws_secret_access_key=args.s3_accesskey,
                                     aws_access_key_id=args.s3_id) as s3client:
        while True:
            consumers = await jsm.consumers_info(args.stream)
            #        print(consumers)
            for consumer in consumers:
                # if consumer.name in existing_consumers:
                #     continue
                # existing_consumers[consumer.name] = True
                #            asyncio.create_task(consume(js, consumer.config.filter_subject, consumer.config.durable_name))
                if (consumer.num_pending > 0):
                    await consume(s3client, args.bucket, js, consumer.config.filter_subject, consumer.config.durable_name)

            time.sleep(3)

    await nc.close()


async def consume(s3client, bucket, js, subject, durable):
    print(f"Starting {subject}, {durable}")
    psub = await js.pull_subscribe(subject, durable=durable)
    while True:
        try:
            msgs = await psub.fetch(10)
        except TimeoutError:
            break
        for msg in msgs:
#            print(msg.data)
            jobdata = json.loads(msg.data)
            print(jobdata)
            response = await s3client.get_object(Bucket=bucket, Key=jobdata['inFile'])
            # this will ensure the connection is correctly re-used/closed
            async with response['Body'] as stream:
                invalue = await stream.read()
            newvalue = int(invalue) + int(jobdata['value'])
            print(f"{int(invalue)} + {jobdata['value']} = {newvalue}")

            resp = await s3client.put_object(Bucket=bucket,
                                             Key=jobdata['outFile'],
                                             Body=str(newvalue).encode(),
                                             ContentType='text/plain')
            print(resp)

            await msg.ack()

    print(f"Finished {subject}, {durable}")

if __name__ == '__main__':
    asyncio.run(main()
)
