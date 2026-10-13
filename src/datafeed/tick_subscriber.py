"""
A sample subscriber to subscribe to tick data published on "ticks" topic
"""

import logging
import msgpack
import zmq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def run_subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")

    # Define what topic you want to subscribe to.
    # To subscribe to everything, use an empty string: socket.setsockopt_string(zmq.SUBSCRIBE, "")
    # topic_filter = "weather"
    socket.setsockopt_string(zmq.SUBSCRIBE,"ticks")

    logger.log(logging.INFO,f"Subscriber connected and listening for tick : ...")

    try:
        while True:
            # This blocks until a matching message is received
            logger.log(logging.INFO, "waiting for message...")
            # Use recv_multipart to get both the topic and the data
            topic, message_bytes = socket.recv_multipart()


            # Decode bytes to string and load back into a Python dictionary
            tick = msgpack.unpackb(message_bytes, raw=False)

            logger.log(logging.INFO, f"Received: {tick}")
    except KeyboardInterrupt:
        logger.log(logging.INFO,"\nShutting down subscriber.")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    run_subscriber()
