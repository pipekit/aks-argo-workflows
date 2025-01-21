import argparse
import asyncio
import nats
import time
from nats.errors import TimeoutError

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nats_address", help="Address of NATS")
    parser.add_argument("stream", help="Stream")
    parser.add_argument("consumer", help="Consumer durable name to wait for")
    args = parser.parse_args()
    nc = await nats.connect(args.nats_address)

    # Access jetstream manager
    jsm = nc.jsm()

    while True:
        consumer = await jsm.consumer_info(args.stream, args.consumer)
        print(consumer)
        if (consumer.num_pending == 0 and consumer.num_ack_pending == 0):
            break
        time.sleep(3)

    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
