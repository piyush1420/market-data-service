import json
import threading
from datetime import datetime
from typing import List
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from app.core.kafka_config import kafka_config
from app.core.database import SessionLocal
from app.models.market_data import ProcessedPrice, MovingAverage

class MovingAverageConsumer:
    def __init__(self):
        self.consumer = kafka_config.get_consumer('ma-consumer-group')
        self.topic = kafka_config.price_events_topic
        self.running = False
        self.thread = None
    
    def start_consuming(self):
        """Start consuming price events in a background thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._consume_loop, daemon=True)
            self.thread.start()
            print("Moving Average consumer started")
    
    def stop_consuming(self):
        """Stop consuming price events"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.consumer.close()
        print("Moving Average consumer stopped")
    
    def _consume_loop(self):
        """Main consumption loop"""
        self.consumer.subscribe([self.topic])
        
        while self.running:
            try:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f'Consumer error: {msg.error()}')
                        continue
                
                # Process the message
                self._process_price_event(msg.value().decode('utf-8'))
                
            except Exception as e:
                print(f"Error in consumer loop: {e}")
                if self.running:
                    continue
                else:
                    break
    
    def _process_price_event(self, message: str):
        """Process a price event and calculate moving average"""
        try:
            event = json.loads(message)
            symbol = event['symbol']
            
            db = SessionLocal()
            try:
                # Calculate 5-point moving average
                ma_5 = self._calculate_moving_average(db, symbol, 5)
                
                if ma_5:
                    # Store moving average
                    ma_record = MovingAverage(
                        symbol=symbol,
                        ma_5=ma_5
                    )
                    db.add(ma_record)
                    db.commit()
                    print(f"Calculated MA(5) for {symbol}: ${ma_5:.2f}")
                
            finally:
                db.close()
                
        except Exception as e:
            print(f"Error processing price event: {e}")
    
    def _calculate_moving_average(self, db: Session, symbol: str, period: int) -> float:
        """Calculate moving average for the last N periods"""
        try:
            # Get last N prices
            prices = db.query(ProcessedPrice).filter(
                ProcessedPrice.symbol == symbol
            ).order_by(ProcessedPrice.timestamp.desc()).limit(period).all()
            
            if len(prices) < period:
                return None
            
            # Calculate average
            total = sum(price.price for price in prices)
            return total / period
            
        except Exception as e:
            print(f"Error calculating moving average: {e}")
            return None

# Global instance
ma_consumer = MovingAverageConsumer()