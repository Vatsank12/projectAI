# VigilantAI - Advanced System Monitoring & Security Dashboard

A modern, real-time system monitoring and security dashboard built with FastAPI, Tailwind CSS, and Chart.js. Features real-time metrics tracking, file security scanning, process monitoring, AI-powered assistant with Groq integration, and alerting system.

## 🎨 Features

### Dashboard
- **Real-Time Metrics**: CPU, Memory, Disk, and Network usage tracking
- **Interactive Charts**: Live-updating performance graphs with Chart.js
- **System Health Score**: AI-calculated health indicator
- **System Information**: CPU cores, RAM, uptime, and storage info

### File Scanner
- **Drag & Drop Interface**: Easy file scanning
- **Concurrent Processing**: Optimized scanning with 4-file batch processing
- **Threat Detection**: Analyzes files for suspicious indicators
- **Hash Analysis**: SHA256 file hashing for verification
- **Directory Scanning**: Full directory tree scanning with progress tracking
- **Abort Functionality**: Cancel scans in progress
- **Quarantine System**: Isolate suspicious files

### Process Monitor
- **Top Processes**: View the most resource-intensive processes
- **Real-Time Updates**: Process list refreshes every 2 seconds
- **Process Details**: Drill down into individual process information
- **Process Management**: Kill processes directly from dashboard

### Security Alerts
- **Real-Time Alerts**: Critical, High, Medium, Low severity levels
- **Color-Coded**: Visual indicators for alert priority
- **Alert History**: View recent security events
- **Auto-Dismiss**: Notifications automatically clear

### AI Assistant
- **Groq AI Integration**: Powered by Groq's Llama-3.1-8B model for intelligent responses
- **Smart Chat Panel**: Get system insights and recommendations
- **Health Analysis**: AI provides health insights and recommendations
- **Overheating Detection**: Automatic PC overheating analysis and solutions
- **Quick Actions**: One-click access to common tasks
- **Chat History**: Persistent conversation history
- **Fallback System**: Local AI when Groq is unavailable

### Settings
- **Monitoring Interval**: Adjust metrics update frequency
- **Alert Thresholds**: Customize CPU and Memory alert limits
- **Sound Alerts**: Enable/disable notification sounds
- **Theme Support**: Dark/cyberpunk theme options

## 🛠️ Tech Stack

**Backend:**
- Python 3.12+
- FastAPI
- psutil (system monitoring)
- Groq AI (intelligent assistant)
- python-dotenv (environment management)
- SQLite (data persistence)
- WebSockets (real-time updates)

**Frontend:**
- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Chart.js (data visualization)
- Animate.css (animations)

## 📋 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Groq API key (free at https://console.groq.com/keys)

### Setup

1. **Clone/Extract the project**
```bash
cd VigilantAI
```

2. **Configure Environment**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# Get free API key at: https://console.groq.com/keys
```

3. **Create virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

1. **Start the backend server**
```bash
cd backend
python main.py
```

The server will start at `http://localhost:8000`

2. **Open in browser**
```
http://localhost:8000
```

3. **Login**
- Username: `admin`
- Password: `admin`

## 📁 Project Structure

```
VigilantAI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── routers/
│   │   ├── metrics.py       # System metrics endpoints
│   │   ├── scanner.py       # File scanning endpoints
│   │   ├── processes.py     # Process monitoring endpoints
│   │   ├── alerts.py        # Alert management
│   │   └── assistant.py     # AI assistant endpoints
│   ├── core/
│   │   └── websocket_manager.py  # WebSocket connection manager
│   └── db/
│       └── models.py        # Database models
├── frontend/
│   ├── index.html           # Login page
│   ├── dashboard.html       # Main dashboard
│   ├── styles.css           # Global styles & animations
│   └── js/
│       ├── main.js          # Core functionality
│       ├── charts.js        # Chart.js integration
│       └── assistant.js     # AI assistant logic
└── README.md
```

## 🎯 API Endpoints

### Metrics
- `GET /api/metrics/current` - Get current system metrics
- `WS /api/metrics/ws/{client_id}` - WebSocket for real-time metrics

### Scanner
- `GET /api/scanner/files` - List scanned files
- `POST /api/scanner/scan` - Scan a single file
- `POST /api/scanner/batch-scan` - Scan multiple files concurrently
- `POST /api/scanner/scan-directory` - Scan entire directory tree
- `GET /api/scanner/progress` - Get scan progress
- `POST /api/scanner/abort` - Abort current scan
- `GET /api/scanner/quarantine` - Get quarantined files
- `POST /api/scanner/quarantine/{hash}` - Quarantine a file
- `DELETE /api/scanner/quarantine/{hash}` - Restore from quarantine

### Processes
- `GET /api/processes/list` - Get top processes
- `GET /api/processes/details/{pid}` - Get process details
- `POST /api/processes/kill/{pid}` - Kill a process
- `GET /api/processes/system-info` - Get system information

### Alerts
- `GET /api/alerts/` - Get all alerts
- `GET /api/alerts/unread` - Get unread alerts
- `POST /api/alerts/{id}/read` - Mark alert as read
- `DELETE /api/alerts/{id}` - Delete alert

### Assistant
- `POST /api/assistant/message` - Send message to AI
- `GET /api/assistant/history` - Get conversation history
- `GET /api/assistant/health-insight` - Get health insights
- `GET /api/assistant/quick-actions` - Get quick actions

## 🎨 UI Themes

The dashboard features a modern cyberpunk theme with:
- **Neon cyan, purple, and green** accent colors
- **Glassmorphism** effects with blur backgrounds
- **Smooth animations** and transitions
- **Responsive design** for all screen sizes
- **Dark mode** optimized for eye comfort

## 🔐 Security Notes

- Default credentials (admin/admin) should be changed in production
- File scanner uses SHA256 hashing for verification
- Suspicious files are quarantined with threat scoring
- System metrics are collected using psutil safely
- CORS is enabled for development

## ⚙️ Configuration

Edit `backend/main.py` to configure:
- **Port**: Change `8000` to desired port
- **Host**: Change `0.0.0.0` to specific IP
- **CORS**: Modify allowed origins for production

## 📊 Monitoring Capabilities

- **CPU Usage**: Real-time processor utilization
- **Memory**: RAM usage and available memory
- **Disk**: Storage usage and I/O statistics
- **Network**: Upload/download speeds and packet data
- **Temperature**: System temperature monitoring
- **Processes**: CPU and memory per-process breakdown

## 🐛 Troubleshooting

**Port already in use:**
```bash
python main.py --port 8001
```

**AI Assistant not responding intelligently:**
- Check that your Groq API key is correctly set in `.env`
- Verify the key is valid at https://console.groq.com/keys
- The system falls back to local AI if Groq is unavailable

**Scan abort button not working:**
- The abort functionality now properly cancels both frontend and backend operations
- Click the abort button during scanning to stop the process

**Slow scanning performance:**
- The scanner now processes files concurrently in batches of 4
- Large directories may still take time due to file I/O operations
- Use the abort button if you need to stop a long scan

**Permission denied errors:**
- Run as administrator (Windows) or with sudo (Linux/macOS)
- Some process operations require elevated privileges

**Frontend not loading:**
- Check that frontend files are in the `frontend/` directory
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for errors (F12)

## 📝 Future Enhancements

- [ ] User authentication system
- [ ] Database persistence for alerts and scan history
- [ ] Email notifications
- [ ] Custom alert rules
- [ ] Performance analytics
- [ ] Export reports
- [ ] Mobile app
- [ ] Dark/Light theme toggle
- [ ] Multi-user support

## 📄 License

This project is provided as-is for educational and personal use.

## 👤 Author

VigilantAI Development Team

## 💬 Support

For issues or questions, please check the documentation or contact support.

---

**Start monitoring and securing your system today with VigilantAI! 🚀**
