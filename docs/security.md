# Security: Rate Limiting

## Overview
Rate limiting has been implemented on authentication endpoints to prevent brute-force attacks.

## Configuration

### Rate Limits
- **Login attempts**: 5 per 15 minutes per IP address
- **Account lockout**: 10 failed attempts in 1 hour
- **Lockout duration**: 1 hour

### Response Headers
All authentication responses include rate limit headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

### Status Codes
- `429 Too Many Requests`: Rate limit exceeded
- `403 Forbidden`: Account temporarily locked

## Monitoring
Alerts are triggered when:
- More than 100 rate limit violations per hour
- Account lockout occurs
- Suspicious IP patterns detected

## Whitelist
Trusted IPs can bypass rate limiting by adding to `security.json`.

## Emergency Disable
To disable rate limiting:
export ENABLE_RATE_LIMITING=false
