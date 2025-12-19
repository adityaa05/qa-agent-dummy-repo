import unittest
from src.auth.login import LoginHandler, RateLimiter

class TestRateLimiter(unittest.TestCase):
    
    def setUp(self):
        self.rate_limiter = RateLimiter(max_attempts=5, window_minutes=15)
    
    def test_allows_requests_under_limit(self):
        """Test that requests under limit are allowed"""
        result = self.rate_limiter.check_rate_limit('192.168.1.1')
        self.assertTrue(result['allowed'])
        self.assertEqual(result['remaining'], 5)
    
    def test_blocks_requests_over_limit(self):
        """Test that requests over limit are blocked"""
        ip = '192.168.1.2'
        for _ in range(5):
            self.rate_limiter.record_attempt(ip, False)
        
        result = self.rate_limiter.check_rate_limit(ip)
        self.assertFalse(result['allowed'])
        self.assertEqual(result['remaining'], 0)


class TestLoginHandler(unittest.TestCase):
    
    def setUp(self):
        self.handler = LoginHandler()
    
    def test_successful_login(self):
        """Test successful authentication"""
        result = self.handler.authenticate('testuser', 'password123', '192.168.1.1')
        self.assertEqual(result['status'], 200)
        self.assertIn('token', result)
    
    def test_rate_limit_exceeded(self):
        """Test that rate limiting works"""
        ip = '192.168.1.3'
        for _ in range(5):
            self.handler.authenticate('testuser', 'wrong', ip)
        
        result = self.handler.authenticate('testuser', 'password123', ip)
        self.assertEqual(result['status'], 429)
