import logging
import yaml
from services.producer import Producer
from services.change_tracker import ChangeTracker


def read_configuration():
    with open("config.yml", "r") as config:
        cfg = yaml.safe_load(config)
    return cfg


if __name__ == '__main__':
    configuration = read_configuration()
    logging.basicConfig(filename='fileTracker.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    logging.info("Running fileTracker app ...")
    rabit_mq_host = configuration["rabitMQ"]["host"]
    rabit_mq_port = configuration["rabitMQ"]["port"]
    queue_name = configuration["rabitMQ"]["queue_name"]
    directory = configuration["directory"]
    producer = Producer(host=rabit_mq_host, port=rabit_mq_port,  queue_name=queue_name)
    change_tracker = ChangeTracker(tracked_dir=directory, producer=producer)
    change_tracker.start()





