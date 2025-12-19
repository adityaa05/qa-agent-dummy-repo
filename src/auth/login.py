import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Dict

class RateLimiter:
    """Rate limiter for login attempts"""
    
    def __init__(self, max_attempts=5, window_minutes=15):
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts = {}  # IP -> [(timestamp, success)]
    
    def check_rate_limit(self, ip_address: str) -> Dict:
        """Check if IP has exceeded rate limit"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=self.window_minutes)
        
        # Clean old attempts
        if ip_address in self.attempts:
            self.attempts[ip_address] = [
                (ts, success) for ts, success in self.attempts[ip_address]
                if ts > cutoff
            ]
        
        attempts_in_window = len(self.attempts.get(ip_address, []))
        
        if attempts_in_window >= self.max_attempts:
            reset_time = self.attempts[ip_address][0][0] + timedelta(minutes=self.window_minutes)
            return {
                'allowed': False,
                'limit': self.max_attempts,
                'remaining': 0,
                'reset': int(reset_time.timestamp())
            }
        
        return {
            'allowed': True,
            'limit': self.max_attempts,
            'remaining': self.max_attempts - attempts_in_window,
            'reset': int((now + timedelta(minutes=self.window_minutes)).timestamp())
        }
    
    def record_attempt(self, ip_address: str, success: bool):
        """Record a login attempt"""
        if ip_address not in self.attempts:
            self.attempts[ip_address] = []
        self.attempts[ip_address].append((datetime.now(), success))


class LoginHandler:
    """Handles user authentication with rate limiting"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter(max_attempts=5, window_minutes=15)
        self.account_lockouts = {}  # user_id -> lockout_until
    
    def authenticate(self, username: str, password: str, ip_address: str) -> Dict:
        """Authenticate user with rate limiting"""
        # Check rate limit
        rate_limit = self.rate_limiter.check_rate_limit(ip_address)
        
        if not rate_limit['allowed']:
            return {
                'status': 429,
                'error': 'Too many login attempts',
                'headers': {
                    'X-RateLimit-Limit': rate_limit['limit'],
                    'X-RateLimit-Remaining': rate_limit['remaining'],
                    'X-RateLimit-Reset': rate_limit['reset']
                }
            }
        
        # Check account lockout
        if self._is_account_locked(username):
            return {
                'status': 403,
                'error': 'Account temporarily locked'
            }
        
        # Validate credentials
        if self._validate_credentials(username, password):
            self.rate_limiter.record_attempt(ip_address, success=True)
            token = self._generate_token(username)
            return {
                'status': 200,
                'token': token,
                'user_id': username
            }
        else:
            self.rate_limiter.record_attempt(ip_address, success=False)
            return {
                'status': 401,
                'error': 'Invalid credentials'
            }
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        return username and password and len(password) >= 8
    
    def _generate_token(self, username: str) -> str:
        payload = f"{username}:{int(time.time())}"
        return hashlib.sha256(payload.encode()).hexdigest()
    
    def _is_account_locked(self, username: str) -> bool:
        if username in self.account_lockouts:
            if datetime.now() < self.account_lockouts[username]:
                return True
            else:
                del self.account_lockouts[username]
        return False
