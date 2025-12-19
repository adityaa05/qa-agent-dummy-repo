# QA Agent Demo Repository

This repository demonstrates automated QA workflow analysis for Pull Requests.

## API Endpoints

### Authentication Endpoints (v2.0)

#### POST /api/v2/login
Authenticates a user and returns a session token.

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "user_id": "string",
  "expires_at": "timestamp"
}
```

#### POST /api/v2/logout
Invalidates the current session token.

**Request Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

## Authentication Flow

1. User submits credentials to /api/v2/login
2. Server validates credentials
3. Server generates session token
4. Client stores token
5. Client includes token in Authorization header for protected endpoints

## Installation
```bash
npm install
npm start
```

## Testing
```bash
npm test
```

## License

MIT License
