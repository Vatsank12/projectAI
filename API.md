# VigilantAI API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently uses simple demo auth. In production, implement JWT or similar.

---

## Metrics Endpoints

### Get Current Metrics
```
GET /api/metrics/current
```

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "cpu": 45.5,
  "memory": {
    "percent": 62.3,
    "used": 16.2,
    "total": 26.0
  },
  "disk": {
    "percent": 45.2,
    "used": 230.5,
    "total": 512.0,
    "read_count": 123456,
    "write_count": 98765
  },
  "network": {
    "bytes_sent": 1024.5,
    "bytes_recv": 2048.3,
    "packets_sent": 1000,
    "packets_recv": 1500
  },
  "temperature": 52.3
}
```

### WebSocket Real-Time Metrics
```
WS /api/metrics/ws/{client_id}
```

Connects to WebSocket stream for continuous metric updates.

---

## Processes Endpoints

### List Top Processes
```
GET /api/processes/list
```

**Response:**
```json
[
  {
    "pid": 1234,
    "name": "chrome.exe",
    "memory_percent": 8.5,
    "cpu_percent": 2.3
  },
  ...
]
```

### Get Process Details
```
GET /api/processes/details/{pid}
```

**Response:**
```json
{
  "pid": 1234,
  "name": "chrome.exe",
  "status": "running",
  "memory_info": {
    "rss": 268435456,
    "vms": 536870912
  },
  "cpu_num": 2,
  "create_time": 1610700000.0,
  "exe": "C:\\Program Files\\Chrome\\chrome.exe",
  "cwd": "C:\\Users\\User"
}
```

### Kill Process
```
POST /api/processes/kill/{pid}
```

**Response:**
```json
{
  "status": "Process killed",
  "pid": 1234
}
```

### Get System Info
```
GET /api/processes/system-info
```

**Response:**
```json
{
  "cpu_count": 8,
  "cpu_freq": {
    "current": 2400.0,
    "min": 800.0,
    "max": 3600.0
  },
  "boot_time": 1610700000.0,
  "uptime_seconds": 86400
}
```

---

## Scanner Endpoints

### Get Scanned Files
```
GET /api/scanner/files
```

**Response:**
```json
[
  {
    "filename": "document.pdf",
    "hash": "abc123...",
    "size": 1024000,
    "threat_score": 15,
    "threat_level": "LOW",
    "suspicious_indicators": [],
    "timestamp": "2024-01-15T10:30:45"
  },
  ...
]
```

### Scan File
```
POST /api/scanner/scan
Content-Type: multipart/form-data

file: <binary>
```

**Response:**
```json
{
  "filename": "malware.exe",
  "hash": "def456...",
  "size": 2048000,
  "threat_score": 85,
  "threat_level": "CRITICAL",
  "suspicious_indicators": [
    "Executable extension detected",
    "Unusually large file"
  ],
  "timestamp": "2024-01-15T10:30:45"
}
```

### Scan Directory
```
POST /api/scanner/scan-directory
Content-Type: application/json

{
  "path": "/path/to/directory"
}
```

**Response:**
```json
{
  "status": "Scan started",
  "path": "/path/to/directory"
}
```

### Get Quarantine Files
```
GET /api/scanner/quarantine
```

**Response:**
```json
[
  {
    "filename": "malware.exe",
    "hash": "def456...",
    "threat_level": "CRITICAL",
    ...
  }
]
```

### Quarantine File
```
POST /api/scanner/quarantine/{file_hash}
```

### Restore from Quarantine
```
DELETE /api/scanner/quarantine/{file_hash}
```

---

## Alerts Endpoints

### Get All Alerts
```
GET /api/alerts/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "High CPU Usage",
    "message": "CPU usage exceeds 80%",
    "severity": "high",
    "type": "performance",
    "timestamp": "2024-01-15T10:30:45",
    "read": false
  },
  ...
]
```

### Get Unread Alerts
```
GET /api/alerts/unread
```

### Mark Alert as Read
```
POST /api/alerts/{alert_id}/read
```

**Response:**
```json
{
  "id": 1,
  "title": "High CPU Usage",
  "read": true
}
```

### Delete Alert
```
DELETE /api/alerts/{alert_id}
```

**Response:**
```json
{
  "status": "Alert deleted"
}
```

### Create Alert
```
POST /api/alerts/create
Content-Type: application/json

{
  "title": "Custom Alert",
  "message": "Alert message",
  "severity": "medium",
  "alert_type": "system"
}
```

### Clear All Alerts
```
DELETE /api/alerts/clear-all
```

**Response:**
```json
{
  "status": "All alerts cleared"
}
```

---

## Assistant Endpoints

### Send Message
```
POST /api/assistant/message
?message=<your_message>
```

**Response:**
```json
{
  "id": 1,
  "user_message": "What is my system health?",
  "ai_response": "Your system health score is 85/100 (HEALTHY)...",
  "timestamp": "2024-01-15T10:30:45"
}
```

### Get Conversation History
```
GET /api/assistant/history
```

**Response:**
```json
[
  {
    "id": 1,
    "user_message": "What is my system health?",
    "ai_response": "Your system health score is...",
    "timestamp": "2024-01-15T10:30:45"
  },
  ...
]
```

### Get Health Insight
```
GET /api/assistant/health-insight
```

**Response:**
```json
{
  "health": {
    "score": 85,
    "status": "HEALTHY",
    "cpu": 45.5,
    "memory": 62.3,
    "disk": 45.2
  },
  "insights": [
    "Your system is running smoothly!"
  ]
}
```

### Get Quick Actions
```
GET /api/assistant/quick-actions
```

**Response:**
```json
[
  {
    "id": 1,
    "label": "Run Full Scan",
    "action": "scan"
  },
  {
    "id": 2,
    "label": "Analyze Processes",
    "action": "processes"
  },
  ...
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid parameter"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting. Implement as needed in production.

## CORS

CORS is enabled for all origins in development. Configure appropriately for production.

## Authentication

Demo uses simple local storage. Implement proper auth for production:
- JWT tokens
- Session management
- API keys
- OAuth 2.0

## Pagination

Not yet implemented. Add pagination for list endpoints in production.

---

## Examples

### JavaScript Fetch

```javascript
// Get metrics
fetch('/api/metrics/current')
  .then(r => r.json())
  .then(data => console.log(data));

// Send assistant message
fetch('/api/assistant/message?message=What%20is%20my%20system%20health%3F')
  .then(r => r.json())
  .then(data => console.log(data.ai_response));
```

### cURL

```bash
# Get current metrics
curl http://localhost:8000/api/metrics/current

# Get processes
curl http://localhost:8000/api/processes/list

# Get alerts
curl http://localhost:8000/api/alerts/

# Send message to AI
curl "http://localhost:8000/api/assistant/message?message=hello"
```

### Python

```python
import requests

# Get metrics
response = requests.get('http://localhost:8000/api/metrics/current')
data = response.json()

# Get processes
response = requests.get('http://localhost:8000/api/processes/list')
processes = response.json()
```

---

## WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/api/metrics/ws/client1');

ws.onmessage = (event) => {
  const metrics = JSON.parse(event.data);
  console.log('CPU:', metrics.cpu);
};

ws.onclose = () => {
  console.log('Connection closed');
};
```

---

## Future Enhancements

- [ ] GraphQL API
- [ ] WebSocket events for real-time updates
- [ ] Rate limiting
- [ ] API versioning
- [ ] OAuth 2.0 authentication
- [ ] OpenAPI 3.0 spec
- [ ] Pagination and filtering
- [ ] Caching layer

---

Last Updated: 2024-01-15
