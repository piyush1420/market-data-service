from app.services.price_producer import price_producer
import time

print("Testing Kafka producer...")
price_producer.publish_price_event("TEST", 100.0, "test_source")
print("Message sent!")
time.sleep(2)
print("Test complete")
