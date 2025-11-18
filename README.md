# VigilantAI - Advanced System Monitoring & Security Dashboard

A comprehensive, real-time system monitoring and security dashboard application built with FastAPI and WebSocket technology. VigilantAI provides advanced threat detection, system health monitoring, and intelligent security scanning capabilities.

## 🎯 Features

### System Monitoring
- **Real-time CPU Usage**: Monitor processor utilization with live updates
- **Memory Management**: Track RAM usage, available memory, and memory trends
- **Disk Analysis**: Monitor storage usage, disk I/O operations, and read/write counts
- **Network Monitoring**: Track bandwidth usage, packet statistics, and network performance
- **System Temperature**: Monitor system temperature and thermal conditions

### Security & Scanning
- **File Scanner**: Comprehensive file analysis with threat detection
- **Malware Analysis**: Identify suspicious files and executable patterns
- **File Quarantine**: Isolate potentially dangerous files for safety
- **File Hash Calculation**: SHA-256 based file integrity verification
- **MIME Type Detection**: Automatic file type classification

### Advanced Features
- **Real-time Alerts**: Configurable alert system for system threshold violations
- **Process Management**: Monitor and manage running processes
- **WebSocket Streaming**: Live metric streaming with persistent connections
- **User Profiles**: Customizable user profiles and preferences
- **Email Notifications**: Optional email alerts for critical events
- **Theme Support**: Light/dark mode theme switching

### API Documentation
- **Interactive Swagger UI**: Available at `/docs`
- **ReDoc Documentation**: Available at `/redoc`
- **RESTful API**: Comprehensive API endpoints for all features
- **Health Check**: System health status endpoint

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **System Monitoring**: psutil 5.9.6
- **AI Integration**: Groq API (4.0.2)
- **Real-time Communication**: WebSockets 12.0
- **File Handling**: aiofiles 23.2.1, python-magic 0.4.27
- **Environment**: python-dotenv 1.0.0
- **File Monitoring**: Watchdog 3.0.0

### Frontend
- **HTML5/CSS3/JavaScript**
- **Real-time Dashboard UI**
- **Responsive Design**
- **Interactive Visualizations**

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB for application and data

## 🚀 Installation & Setup

### Prerequisites
Ensure Python 3.8+ is installed on your system:
```bash
python --version
```

### 1. Clone the Repository
```bash
git clone https://github.com/Vatsank12/projectAI.git
cd projectAI/VigilantAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

For development with additional backend dependencies:
```bash
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root directory:
```bash
# Server Configuration
ENVIRONMENT=development
HOST=127.0.0.1
PORT=8000

# Groq API Configuration (for AI features)
GROQ_API_KEY=your_groq_api_key_here

# Alert Thresholds (optional)
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85
DISK_THRESHOLD=90
TEMPERATURE_THRESHOLD=85
```

### 4. Run the Application
```bash
python backend/main.py
```

The application will start with the following output:
```
======================================================================
  VigilantAI - System Monitoring & Security Dashboard v1.0.0
======================================================================
Access Dashboard:
   -> http://localhost:8000

Demo Credentials:
   Username: admin
   Password: admin

API Documentation:
   -> http://localhost:8000/docs
   -> http://localhost:8000/redoc

Health Check:
   -> http://localhost:8000/health

Press Ctrl+C to stop the server
======================================================================
```

## 📊 API Endpoints

### Metrics API
- `GET /api/metrics/current` - Get current system metrics
- `GET /api/metrics/history` - Get historical metrics data
- `WebSocket /api/metrics/stream` - Real-time metrics streaming

### Scanner API
- `POST /api/scanner/upload` - Upload and scan files
- `GET /api/scanner/results` - Get scan results
- `GET /api/scanner/quarantine` - View quarantined files
- `POST /api/scanner/restore` - Restore quarantined files
- `GET /api/scanner/status` - Get scanner status

### Processes API
- `GET /api/processes` - List all running processes
- `POST /api/processes/terminate` - Terminate a process
- `GET /api/processes/{pid}` - Get process details

### Alerts API
- `GET /api/alerts` - Retrieve system alerts
- `POST /api/alerts/create` - Create custom alert
- `DELETE /api/alerts/{id}` - Clear alerts

### Profile API
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile settings
- `POST /api/profile/preferences` - Update user preferences

### System Health
- `GET /health` - Health check endpoint
- `GET /info` - Application information
- `GET /` - Dashboard page
- `GET /dashboard` - Dashboard page

## 🎨 Dashboard Features

### Real-time Monitoring
- Live CPU, Memory, and Disk usage graphs
- Network bandwidth visualization
- System temperature monitoring
- Process list with resource allocation

### Security Dashboard
- File scanning interface
- Quarantine management
- Threat detection results
- File analysis reports

### User Experience
- Dark/Light theme toggle
- Sound alerts for critical events
- Email notification configuration
- Customizable alert thresholds

## 📁 Project Structure

```
VigilantAI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── routers/
│   │   ├── metrics.py       # System metrics endpoints
│   │   ├── scanner.py       # File scanning endpoints
│   │   ├── processes.py     # Process management endpoints
│   │   ├── alerts.py        # Alert system endpoints
│   │   ├── profile.py       # User profile endpoints
│   │   └── assistant.py     # AI assistant endpoints
│   ├── core/
│   │   └── websocket_manager.py  # WebSocket connection manager
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── index.html          # Main dashboard
│   ├── styles.css          # Dashboard styling
│   └── js/                 # JavaScript components
├── requirements.txt        # Main dependencies
└── README.md              # This file
```

## 🔒 Security Features

- **File Hash Verification**: SHA-256 based file integrity checking
- **Threat Detection**: Identifies suspicious file extensions and locations
- **Quarantine System**: Safely isolates potentially dangerous files
- **MIME Type Validation**: Ensures safe file type handling
- **CORS Protection**: Cross-Origin Resource Sharing configured
- **Input Validation**: Request validation for all endpoints

## ⚙️ Configuration

### Alert Thresholds
Alert thresholds are configurable in `backend/config.py`:
```python
ALERT_THRESHOLDS = {
    "cpu": 80,           # Alert when CPU exceeds 80%
    "memory": 85,        # Alert when RAM exceeds 85%
    "disk": 90,          # Alert when disk exceeds 90%
    "temperature": 85    # Alert when temperature exceeds 85°C
}
```

### Monitoring Interval
Default monitoring interval is 1 second (can be adjusted in config):
```python
MONITORING_INTERVAL = 1  # seconds
```

## 📈 Performance Considerations

- **Metric History**: Maintains last 60 data points per metric
- **Concurrent Connections**: Supports multiple WebSocket connections
- **File Scanning**: Multi-threaded scanning with 4 worker threads
- **Memory Efficient**: Capped history prevents unbounded memory growth

## 🐛 Troubleshooting

### Frontend Not Loading
- Ensure the `frontend` directory exists in the project root
- Check that `index.html` is present in the frontend folder
- Verify frontend path: `http://localhost:8000`

### API Not Responding
- Verify the server is running: `http://localhost:8000/health`
- Check port 8000 is not in use: `netstat -an | grep 8000`
- Review uvicorn logs for errors

### High CPU Usage
- Check for long-running scans in progress
- Monitor process list for resource-intensive operations
- Consider increasing monitoring interval if needed

## 📝 Demo Credentials

For initial setup and testing:
- **Username**: admin
- **Password**: admin

## 🔑 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| ENVIRONMENT | development | Application environment |
| HOST | 127.0.0.1 | Server host address |
| PORT | 8000 | Server port number |
| GROQ_API_KEY | - | API key for Groq AI integration |
| CPU_THRESHOLD | 80 | CPU alert threshold (%) |
| MEMORY_THRESHOLD | 85 | Memory alert threshold (%) |
| DISK_THRESHOLD | 90 | Disk alert threshold (%) |
| TEMPERATURE_THRESHOLD | 85 | Temperature alert threshold (°C) |

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- All new features include appropriate error handling
- API changes are documented
- Security best practices are maintained

## 📄 License

This project is provided as-is for educational and monitoring purposes.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `http://localhost:8000/docs`
3. Check application logs for error messages
4. Verify all dependencies are correctly installed

## 🎓 Educational Purpose

VigilantAI is designed as an advanced educational project demonstrating:
- Real-time system monitoring techniques
- WebSocket-based real-time communication
- FastAPI best practices
- File security and scanning concepts
- System administration fundamentals

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Active Development
