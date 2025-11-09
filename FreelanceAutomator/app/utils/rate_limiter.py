import time
from functools import wraps
from app.utils.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            self.calls = [call for call in self.calls if call > now - self.period]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                logger.warning(f'Rate limit reached. Sleeping for {sleep_time:.2f} seconds')
                time.sleep(sleep_time)
                self.calls = []
            
            self.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
