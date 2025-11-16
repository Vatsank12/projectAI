# VigilantAI - Quick Start Guide

## ⚡ Quick Setup (1 minute)

### Windows
1. Double-click `run.bat`
2. Wait for the server to start
3. Open `http://localhost:8000` in your browser
4. Login with `admin` / `admin`

### Linux/macOS
1. Open terminal in project directory
2. Run: `chmod +x run.sh && ./run.sh`
3. Open `http://localhost:8000` in your browser
4. Login with `admin` / `admin`

## 🚀 Manual Setup

### Step 1: Create Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
python main.py
```

### Step 4: Access Dashboard
- Open `http://localhost:8000` in your browser
- Login credentials: `admin` / `admin`

## 📊 What You Can Do

### Dashboard
- View real-time CPU, Memory, Disk, and Network usage
- See system health score
- Watch live updating charts
- Monitor uptime and system info

### Processes
- View top resource-consuming processes
- See CPU and memory usage per process
- Click to get detailed process information

### File Scanner
- Drag and drop files to scan
- Detect suspicious files
- View threat levels and analysis
- Quarantine dangerous files

### Alerts
- Monitor system alerts
- View alert history
- Filter by severity (Critical, High, Medium, Low)
- Auto-dismissing notifications

### AI Assistant
- Chat with intelligent assistant
- Get system recommendations
- Analyze system health
- Quick action buttons

### Settings
- Adjust monitoring intervals
- Set alert thresholds
- Configure notifications
- Theme preferences

## 🔐 Demo Credentials

```
Username: admin
Password: admin
```

## 🌐 Access Points

| Page | URL |
|------|-----|
| Login | `http://localhost:8000/` |
| Dashboard | `http://localhost:8000/dashboard` |
| API Docs | `http://localhost:8000/docs` |

## 📝 Default Thresholds

- **CPU Alert**: 80%
- **Memory Alert**: 85%
- **Disk Alert**: 90%
- **Monitoring Interval**: 1 second
- **Sound Alerts**: Enabled

## 🐛 Common Issues

### Port Already in Use
If port 8000 is already in use, edit `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to different port
```

### Permission Denied
Run as administrator:
- **Windows**: Right-click and "Run as administrator"
- **Linux/macOS**: Use `sudo ./run.sh`

### Python Not Found
Ensure Python 3.8+ is installed:
```bash
python --version  # Should be 3.8 or higher
```

### Import Errors
Reinstall dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ Mobile browsers (responsive but limited features)

## 🔗 API Base URL

```
http://localhost:8000/api/
```

## 📚 Key APIs

```bash
# Get current metrics
GET /api/metrics/current

# Get processes
GET /api/processes/list

# Get alerts
GET /api/alerts/

# Send message to AI
POST /api/assistant/message?message=<your-question>

# Get alerts
GET /api/alerts/
```

## 💾 Database

SQLite database is created automatically at:
```
backend/vigilant_ai.db
```

To reset database, delete the file and restart the server.

## 📊 System Requirements

- **RAM**: Minimum 256MB, Recommended 512MB+
- **CPU**: Any modern processor
- **Disk**: 50MB free space
- **OS**: Windows, Linux, macOS
- **Python**: 3.8 or higher

## ⚙️ Advanced Configuration

Edit `backend/main.py` to customize:

```python
# Change host and port
uvicorn.run(app, host="0.0.0.0", port=8000)

# Enable/disable CORS
# app.add_middleware(CORSMiddleware, ...)
```

## 🎯 Next Steps

1. ✅ Start the server
2. ✅ Access the dashboard
3. ✅ Explore the features
4. ✅ Customize settings
5. ✅ Check file scanner
6. ✅ Interact with AI assistant

## 💡 Tips

- Use dark mode browser for better cyberpunk theme experience
- Install on local machine for full system monitoring
- Check alerts regularly for security insights
- Run file scanner on suspicious files
- Use AI assistant for system recommendations

## 📞 Support

If you encounter issues:
1. Check console errors (F12)
2. Review the detailed README.md
3. Check port availability
4. Verify Python version
5. Reinstall dependencies

---

**Ready to monitor your system? Start now with just 1 click! 🚀**

```bash
# Windows
run.bat

# Linux/macOS
./run.sh
```
