import functools
import inspect
import logging

import msgpack
import zmq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class ZMQPublisher:
    def __init__(self, endpoint="tcp://*:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(endpoint)

    def publish(self, topic, data):
        logger.log(logging.INFO,"publishing to {}".format(topic))
        self.socket.send_multipart([topic.encode('utf-8'), data])

    def publishZMQtopic(self, topic):
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    result = await func(*args, **kwargs)
                    self.publish(topic, result)
                    return result

                return async_wrapper

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.publish(topic, result)
                return result

            return sync_wrapper

        return decorator

    def close(self):
        self.socket.close()
        # Context.instance() is shared; do not terminate it here.