from confluent_kafka import Producer, Consumer, KafkaError
import json
import os
from typing import Dict, Any, Optional

class KafkaConfig:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.price_events_topic = 'price-events'
    
    def get_producer(self) -> Producer:
        """Get Kafka producer instance"""
        config = {
            'bootstrap.servers': self.bootstrap_servers,
            'client.id': 'market-data-producer'
        }
        return Producer(config)
    
    def get_consumer(self, group_id: str = 'market-data-consumers') -> Consumer:
        """Get Kafka consumer instance"""
        config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True
        }
        return Consumer(config)

# Global instance
kafka_config = KafkaConfig()