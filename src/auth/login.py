

def authenticate_user(username, password):
    """Authenticate user credentials"""
    if not username or not password:
        raise ValueError("Credentials required")
    
    # Validate against database
    user = db.get_user(username)
    
    if not user:
        return False
    
    # NEW: Add rate limiting
    if check_rate_limit(username):
        raise Exception("Too many login attempts")
    
    return verify_password(user, password)

def check_rate_limit(username):
    """Check if user exceeded login rate limit"""
    attempts = cache.get(f"login_attempts:{username}")
    return attempts and attempts > 5
