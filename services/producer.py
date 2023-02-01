import pika


class Producer:
    def __init__(self, host: str, port: int,  queue_name: str):
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.channel = None
        self._connect()

    def _connect(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=self.host, port=self.port))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        self.channel = channel

    def send(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

