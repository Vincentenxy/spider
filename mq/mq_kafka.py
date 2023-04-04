import json
import logging

from kafka import KafkaProducer


# kafak生产者类
class MqKafka(object):
    def __init__(self):
        self.server = '192.168.68.111:9092'
        self.topic = 'test'
        self.producer = None

    # 创建生产者
    def create_producer(self):
        if self.producer:
            return self.producer
        self.producer = KafkaProducer(bootstrap_servers=self.server,
                                        value_serializer=lambda m: json.dumps(m, ensure_ascii=False).encode(),
                                    )
        if self.producer is None:
            logging.info("创建kafka producer 失败")
            return None
        return self.producer

    # 发送数据
    def send_msg(self, topic, content):
        # 主题为空的时候使用默认主题
        if topic is None or topic == '':
            topic = self.topic
        future = self.producer.send(topic=topic, value=content)
        return future.get(timeout=10)
