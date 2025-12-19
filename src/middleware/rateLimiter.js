const redis = require('redis');

class RateLimiterMiddleware {
  constructor(options = {}) {
    this.maxAttempts = options.maxAttempts || 5;
    this.windowMinutes = options.windowMinutes || 15;
    this.client = redis.createClient(options.redisUrl);
    this.whitelist = new Set(options.whitelist || []);
  }

  async middleware(req, res, next) {
    const ip = req.ip || req.connection.remoteAddress;

    // Check whitelist
    if (this.whitelist.has(ip)) {
      return next();
    }

    const key = `rate_limit:${ip}`;
    
    try {
      const current = await this.client.incr(key);
      
      if (current === 1) {
        await this.client.expire(key, this.windowMinutes * 60);
      }

      const ttl = await this.client.ttl(key);
      const resetTime = Math.floor(Date.now() / 1000) + ttl;

      // Set rate limit headers
      res.setHeader('X-RateLimit-Limit', this.maxAttempts);
      res.setHeader('X-RateLimit-Remaining', Math.max(0, this.maxAttempts - current));
      res.setHeader('X-RateLimit-Reset', resetTime);

      if (current > this.maxAttempts) {
        return res.status(429).json({
          error: 'Too Many Requests',
          message: `Rate limit exceeded. Try again in ${Math.ceil(ttl / 60)} minutes.`,
          retryAfter: ttl
        });
      }

      next();
    } catch (error) {
      console.error('Rate limiter error:', error);
      next();
    }
  }
}

module.exports = RateLimiterMiddleware;
