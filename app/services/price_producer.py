import json
import uuid
from datetime import datetime
from typing import Dict, Any
from confluent_kafka import Producer
from app.core.kafka_config import kafka_config

class PriceProducer:
    def __init__(self):
        self.producer = kafka_config.get_producer()
        self.topic = kafka_config.price_events_topic
    
    def publish_price_event(self, symbol: str, price: float, source: str, raw_response_id: str = None):
        """Publish a price event to Kafka"""
        
        if not raw_response_id:
            raw_response_id = str(uuid.uuid4())
        
        event = {
            "symbol": symbol.upper(),
            "price": price,
            "timestamp": datetime.now().isoformat() + "Z",
            "source": source,
            "raw_response_id": raw_response_id
        }
        
        try:
            # Produce message
            self.producer.produce(
                topic=self.topic,
                key=symbol.upper(),
                value=json.dumps(event),
                callback=self._delivery_callback
            )
            
            # Wait for message delivery
            self.producer.flush()
            print(f"Published price event for {symbol}: ${price}")
            
        except Exception as e:
            print(f"Failed to publish price event for {symbol}: {e}")
    
    def _delivery_callback(self, err, msg):
        """Callback for message delivery confirmation"""
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Global instance
price_producer = PriceProducer()