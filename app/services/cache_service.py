import redis
import json
import os
from typing import Optional, Dict, Any

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )
        self.default_ttl = 300  # 5 minutes
    
    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get cached price data"""
        try:
            cached_data = self.redis_client.get(f"price:{symbol.upper()}")
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set_price(self, symbol: str, price_data: Dict[str, Any], ttl: int = None):
        """Cache price data"""
        try:
            if not ttl:
                ttl = self.default_ttl
            
            self.redis_client.setex(
                f"price:{symbol.upper()}", 
                ttl, 
                json.dumps(price_data)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def get_health(self) -> bool:
        """Check if Redis is healthy"""
        try:
            self.redis_client.ping()
            return True
        except:
            return False

# Global instance
cache_service = CacheService()