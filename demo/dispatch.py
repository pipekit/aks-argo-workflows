import argparse
import asyncio
import json
import nats
from nats.errors import TimeoutError

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nats_address", help="Address of NATS")
    parser.add_argument("subject", help="Subject to dispatch to")
    parser.add_argument("count", help="Count of messages to send", type=int)
    parser.add_argument("stepMult", help="Multiplier applied to counted number", type=int)
    parser.add_argument("inputPath", help="S3 path to read from")
    parser.add_argument("outputPath", help="S3 path to write to")

    args = parser.parse_args()
    nc = await nats.connect(args.nats_address)

    # Create JetStream context.
    js = nc.jetstream()

    for i in range(0, args.count):
        data = {
            "inFile": f"{args.inputPath}/{i}.txt",
            "outFile": f"{args.outputPath}/{i}.txt",
            "value": f"{i*args.stepMult}"
        }
        ack = await js.publish(args.subject, json.dumps(data).encode())
        print(ack)

    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
