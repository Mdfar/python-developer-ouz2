import json from aiokafka import AIOKafkaProducer import asyncio

class KafkaProducerService: def init(self): self.bootstrap_servers = 'kafka:9092' self.producer = None

async def _get_producer(self):
    if not self.producer:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
    return self.producer

async def send_to_topic(self, topic: str, data: list):
    prod = await self._get_producer()
    try:
        for record in data:
            await prod.send_and_wait(topic, record)
    finally:
        # In production, we keep the producer alive for reuse
        pass