import pika
import json
import sys

class AbstractMessageQueue():
    channel = None
    exchange = None
    queue_name = None

    def __init__(self, connectingHost, exchangeType):
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=connectingHost)
                    )
        self.channel = connection.channel()
        self.exchange = exchangeType+'_message'
        self.channel.exchange_declare(exchange=self.exchange, type=exchangeType)

    def publish(self, route_key, message):
      message = json.dumps(message)
      try:
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=route_key,
                                   body=message
                                  )
        return True
      except Exception as err:
        sys.stderr.write("Connection Expired. Will try to save the state.")
        return False

    def bind_listener(self, route_key):
      if not self.queue_name:
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        print self.queue_name
      self.channel.queue_bind(exchange=self.exchange,
                     queue=self.queue_name,
                     routing_key=route_key)

    def consumer_callback(self, ch, method, properties, body):
      print(" # Received key '%r' with payload %r" % (method.routing_key, body))

    def consumer(self):
      self.channel.basic_consume(self.consumer_callback,
                      queue=self.queue_name,
                      no_ack=True)
      return self.channel