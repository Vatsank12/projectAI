# VigilantAI - Complete Project Structure

## 📁 Directory Layout

```
VigilantAI/
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # Quick start guide (1 minute setup)
├── 📄 API.md                             # Complete API documentation
├── 📄 PROJECT_STRUCTURE.md               # This file
├── 📄 .gitignore                         # Git ignore patterns
├── 📄 run.bat                            # Windows startup script
├── 📄 run.sh                             # Linux/macOS startup script
├── 📄 .dist/                             # Distribution files
│
├── 📁 backend/                           # Python FastAPI Backend
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 main.py                        # FastAPI application entry point
│   ├── 📄 requirements.txt                # Python dependencies
│   │
│   ├── 📁 routers/                       # API route handlers
│   │   ├── 📄 __init__.py
│   │   ├── 📄 metrics.py                 # System metrics endpoints
│   │   ├── 📄 scanner.py                 # File scanning endpoints
│   │   ├── 📄 processes.py               # Process monitoring endpoints
│   │   ├── 📄 alerts.py                  # Alert management endpoints
│   │   └── 📄 assistant.py               # AI assistant endpoints
│   │
│   ├── 📁 core/                          # Core functionality
│   │   ├── 📄 __init__.py
│   │   └── 📄 websocket_manager.py       # WebSocket connection manager
│   │
│   ├── 📁 db/                            # Database layer
│   │   ├── 📄 __init__.py
│   │   └── 📄 models.py                  # Database models and initialization
│   │
│   └── 📁 utils/                         # Utility functions
│       ├── 📄 __init__.py
│       └── 📄 helpers.py                 # Helper functions
│
└── 📁 frontend/                          # HTML/CSS/JavaScript Frontend
    ├── 📄 index.html                     # Login page
    ├── 📄 dashboard.html                 # Main dashboard
    ├── 📄 styles.css                     # Global CSS & animations
    │
    └── 📁 js/                            # JavaScript modules
        ├── 📄 main.js                    # Core dashboard functionality
        ├── 📄 charts.js                  # Chart.js integration
        └── 📄 assistant.js               # AI assistant logic
```

## 📊 File Count Summary

| Directory | Files | Type |
|-----------|-------|------|
| Root | 8 | Config & Scripts |
| backend | 1 | Python |
| backend/routers | 6 | Python |
| backend/core | 2 | Python |
| backend/db | 2 | Python |
| backend/utils | 2 | Python |
| frontend | 1 | HTML |
| frontend/js | 3 | JavaScript |
| **Total** | **27** | **Mixed** |

## 🔧 Key Files Description

### Backend Files

#### `backend/main.py`
- FastAPI application entry point
- Mounts static frontend files
- Includes all API routers
- WebSocket event handlers
- CORS middleware configuration

#### `backend/routers/metrics.py`
- Real-time CPU, Memory, Disk metrics
- Network usage tracking
- Temperature monitoring
- WebSocket streaming endpoint

#### `backend/routers/scanner.py`
- File upload and scanning
- SHA256 hash calculation
- Threat detection engine
- Quarantine management
- Directory scanning support

#### `backend/routers/processes.py`
- System process enumeration
- Process details retrieval
- Process termination
- System information endpoints

#### `backend/routers/alerts.py`
- Alert creation and management
- Severity classification
- Alert history tracking
- Mark as read functionality

#### `backend/routers/assistant.py`
- AI response generation
- System health analysis
- Quick action suggestions
- Conversation history

#### `backend/core/websocket_manager.py`
- WebSocket connection management
- Broadcast messaging
- Personal messaging
- Connection cleanup

#### `backend/db/models.py`
- SQLite database initialization
- User model
- Scan results table
- Alerts table
- Settings storage
- Metrics history

#### `backend/utils/helpers.py`
- Byte formatting utilities
- Health score calculation
- Threat level classification
- Data sanitization
- Threshold checking

### Frontend Files

#### `frontend/index.html`
- Modern login interface
- Cyberpunk theme application
- Animated particle background
- Form validation
- Session management

#### `frontend/dashboard.html`
- Main dashboard layout
- Navigation sidebar
- Real-time metric cards
- Multi-section layout (Dashboard, Processes, Scanner, Alerts, Settings)
- Floating AI assistant button
- Chart containers

#### `frontend/styles.css`
- Complete cyberpunk theme styling
- Glassmorphism effects
- Smooth animations and transitions
- Responsive design
- Custom scrollbars
- Neon color scheme
- Status badges

#### `frontend/js/main.js`
- Dashboard initialization
- Metric fetching and display
- Chart updates
- Section navigation
- File scanner drag-and-drop
- Process monitoring
- Alert loading
- Assistant messaging

#### `frontend/js/charts.js`
- Chart.js initialization
- Performance chart (CPU/Memory)
- Network chart (Upload/Download)
- Real-time data updates
- Chart animation handling

#### `frontend/js/assistant.js`
- Conversation history loading
- Health insights retrieval
- Quick actions management
- Message history display

## 📦 Dependencies

### Python (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
psutil==5.9.6
watchdog==3.0.0
python-magic==0.4.27
aiofiles==23.2.1
python-multipart==0.0.6
websockets==12.0
```

### Frontend (CDN)
- Tailwind CSS v3
- Chart.js
- Animate.css
- Google Fonts

## 🔌 API Endpoints Structure

```
/api/
├── /metrics/
│   ├── GET /current
│   └── WS /ws/{client_id}
├── /processes/
│   ├── GET /list
│   ├── GET /details/{pid}
│   ├── POST /kill/{pid}
│   └── GET /system-info
├── /scanner/
│   ├── GET /files
│   ├── POST /scan
│   ├── POST /scan-directory
│   ├── GET /quarantine
│   ├── POST /quarantine/{hash}
│   └── DELETE /quarantine/{hash}
├── /alerts/
│   ├── GET /
│   ├── GET /unread
│   ├── POST /{id}/read
│   ├── DELETE /{id}
│   ├── POST /create
│   └── DELETE /clear-all
└── /assistant/
    ├── POST /message
    ├── GET /history
    ├── GET /health-insight
    └── GET /quick-actions
```

## 🎨 Frontend Sections

1. **Dashboard** - Real-time metrics and charts
2. **Processes** - System process monitoring
3. **Scanner** - File security scanning
4. **Alerts** - Security alerts and events
5. **Settings** - Configuration options
6. **Assistant** - AI chat panel (floating)

## 💾 Database Schema

### users
```sql
- id (PRIMARY KEY)
- username (UNIQUE)
- password
- created_at
```

### scan_results
```sql
- id (PRIMARY KEY)
- filename
- file_hash
- threat_level
- threat_score
- timestamp
```

### alerts
```sql
- id (PRIMARY KEY)
- title
- message
- severity
- alert_type
- read
- timestamp
```

### settings
```sql
- id (PRIMARY KEY)
- key (UNIQUE)
- value
- updated_at
```

### metrics_history
```sql
- id (PRIMARY KEY)
- cpu_usage
- memory_usage
- disk_usage
- temperature
- timestamp
```

## 🚀 Startup Sequence

1. **Backend Initialization**
   - FastAPI app created
   - Routes registered
   - CORS middleware added
   - Static files mounted
   - Database initialized

2. **Frontend Loading**
   - HTML parsed
   - CSS loaded
   - JavaScript executed
   - Charts initialized
   - WebSocket connected

3. **Data Streaming**
   - Metrics fetched every 1 second
   - Processes updated every 2 seconds
   - Alerts fetched every 3 seconds
   - Charts updated in real-time

## 📝 Configuration Files

- `requirements.txt` - Python dependencies
- `.gitignore` - Git exclude patterns
- `main.py` - FastAPI configuration
- `dashboard.html` - Frontend configuration

## 🔐 Security Considerations

- ✅ Demo auth implemented
- ⚠️ Should use JWT in production
- ✅ File hash validation
- ✅ Threat scoring algorithm
- ⚠️ CORS should be restricted in production
- ✅ Process isolation maintained

## 📈 Performance Optimizations

- ✅ Real-time WebSocket updates
- ✅ Chart.js with animation throttling
- ✅ Efficient process filtering
- ✅ Lazy-loaded components
- ✅ CSS animations with GPU acceleration
- ✅ Responsive image/font loading

## 🔄 Data Flow

```
Browser → Frontend JS → FastAPI Routes → Backend Logic → System APIs
                                            ↓
                                       Database (SQLite)
                                            ↓
                                    WebSocket Stream ← Browser
```

## 📱 Responsive Design

- **Desktop**: Full feature set
- **Tablet**: Adjusted grid layout
- **Mobile**: Simplified navigation

## 🎯 Key Features Implementation

- ✅ Real-time metrics streaming
- ✅ File threat detection
- ✅ Process monitoring
- ✅ Alert system
- ✅ AI assistant
- ✅ Settings panel
- ✅ Cyberpunk UI theme
- ✅ Charts and visualizations

## 🔗 External Resources

- Tailwind CSS: https://tailwindcss.com
- Chart.js: https://www.chartjs.org
- FastAPI: https://fastapi.tiangolo.com
- psutil: https://psutil.readthedocs.io

---

**Project Version**: 1.0.0
**Last Updated**: January 2024
**Status**: ✅ Complete & Functional
