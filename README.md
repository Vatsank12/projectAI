# VigilantAI

Advanced System Monitoring & Security Dashboard

## Overview

VigilantAI is a comprehensive system monitoring and security dashboard built with FastAPI (backend) and HTML/CSS/JavaScript (frontend). It provides real-time monitoring of system metrics, process management, file scanning for threats, and alert management. The application is designed for system administrators and security professionals to keep track of system health and detect potential threats.

## Features

- **Real-time Metrics Monitoring**: Track CPU usage, memory consumption, disk I/O, network activity, and system temperature in real-time using WebSockets for live updates.
- **Process Management**: View, monitor, and control running processes on the system, including the ability to terminate or kill processes.
- **File Security Scanner**: Scan individual files or entire directories for potential threats based on file extensions, sizes, locations, and other indicators. Includes quarantine functionality for suspicious files.
- **Alerts System**: Create, view, and manage alerts for system events, security issues, performance problems, and process-related notifications.
- **User Authentication**: Simple login system for accessing the dashboard (demo credentials provided).
- **Responsive Web Dashboard**: Clean, modern web interface built with HTML, CSS, and JavaScript for easy monitoring and management.
- **RESTful API**: Comprehensive API with automatic documentation via Swagger UI and ReDoc.
- **Docker Support**: Containerized deployment using Docker and Docker Compose for easy setup and scalability.
- **Health Checks**: Built-in health endpoints for monitoring application status.

## Installation

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- Git (for cloning the repository)

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vatsank12/projectAI.git
   cd VigilantAI
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python backend/main.py
   ```
   Or use the provided batch file:
   ```bash
   run.bat
   ```

The application will start on `http://localhost:8000`.

### Docker Installation

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

This will start the application and an nginx proxy, accessible at `http://localhost:80`.

## Usage

1. **Access the Dashboard**:
   Open your browser and navigate to `http://localhost:8000` (or `http://localhost:80` if using Docker).

2. **Login**:
   Use the demo credentials:
   - Username: `admin`
   - Password: `admin`

3. **Navigate the Dashboard**:
   - **Home**: Overview of system metrics
   - **Processes**: Manage running processes
   - **Scanner**: Scan files and directories for threats
   - **Alerts**: View and manage system alerts

4. **API Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Metrics
- `GET /api/metrics/current` - Retrieve current system metrics
- `WS /api/metrics/ws/{client_id}` - WebSocket endpoint for real-time metrics streaming

### Processes
- `GET /api/processes/` - List all running processes
- `GET /api/processes/{pid}` - Get detailed information about a specific process
- `POST /api/processes/{pid}/kill` - Forcefully terminate a process
- `POST /api/processes/{pid}/terminate` - Gracefully terminate a process

### Scanner
- `POST /api/scanner/scan` - Scan an uploaded file for threats
- `POST /api/scanner/scan-directory` - Initiate a directory scan
- `POST /api/scanner/batch-scan` - Scan multiple uploaded files
- `GET /api/scanner/files` - Retrieve list of scanned files
- `GET /api/scanner/quarantine` - View quarantined files
- `GET /api/scanner/progress` - Check scan progress
- `POST /api/scanner/abort` - Abort an ongoing scan
- `POST /api/scanner/quarantine/{file_hash}` - Quarantine a file
- `DELETE /api/scanner/quarantine/{file_hash}` - Restore a file from quarantine

### Alerts
- `GET /api/alerts/` - Get all alerts
- `GET /api/alerts/unread` - Get unread alerts
- `POST /api/alerts/create` - Create a new alert
- `POST /api/alerts/{alert_id}/read` - Mark an alert as read
- `DELETE /api/alerts/{alert_id}` - Delete an alert
- `DELETE /api/alerts/clear-all` - Clear all alerts

### Health and Info
- `GET /health` - Application health check
- `GET /info` - Application information

## Configuration

The application uses environment variables for configuration (defined in `docker-compose.yml` for Docker deployments):

- `ENVIRONMENT`: Set to `production` for production deployments
- `HOST`: Host address (default: `0.0.0.0`)
- `PORT`: Port number (default: `8000`)

## Deployment

### Production Deployment

1. **Using Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Environment Variables**:
   Set `ENVIRONMENT=production` in your environment or `docker-compose.yml`.

3. **Nginx Proxy**:
   The Docker setup includes an nginx container for reverse proxy and static file serving.

### Manual Deployment

1. Install dependencies and run the application as described in the installation section.
2. Use a process manager like `systemd` or `supervisor` for production.
3. Configure a reverse proxy (nginx/apache) for static file serving and SSL termination.

## Development

### Project Structure
```
VigilantAI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── core/
│   │   └── websocket_manager.py  # WebSocket connection management
│   └── routers/
│       ├── metrics.py       # Metrics monitoring endpoints
│       ├── processes.py     # Process management endpoints
│       ├── scanner.py       # File scanning endpoints
│       ├── alerts.py        # Alert management endpoints
│       └── profile.py       # User profile endpoints
├── frontend/
│   ├── index.html           # Login page
│   ├── dashboard.html       # Main dashboard
│   ├── styles.css           # CSS styles
│   └── js/
│       ├── main.js          # Main JavaScript
│       ├── charts.js        # Chart rendering
│       └── assistant.js     # AI assistant functionality
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── run.bat                  # Windows batch script for running
├── verify_setup.py          # Setup verification script
└── .gitignore               # Git ignore file
```

### Running Tests

Currently, no automated tests are implemented. Manual testing can be performed by:

1. Running the application locally
2. Testing API endpoints using the Swagger UI
3. Verifying frontend functionality in the browser

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused on single responsibilities

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

### Guidelines
- Ensure code quality and add comments where necessary
- Test your changes thoroughly
- Update documentation if needed
- Follow the existing code style

## Security Considerations

- The demo credentials should be changed in production
- Implement proper authentication and authorization
- Use HTTPS in production
- Regularly update dependencies for security patches
- Monitor file permissions and access controls

## Troubleshooting

### Common Issues

1. **Frontend not loading**: Ensure the `frontend` directory exists and contains the required files.
2. **WebSocket connection issues**: Check firewall settings and ensure port 8000 is open.
3. **Permission errors**: Run the application with appropriate permissions for system monitoring.
4. **Docker build failures**: Ensure Docker is properly installed and has access to the project directory.

### Logs

Application logs are output to the console. For Docker deployments, use:
```bash
docker-compose logs vigilantai
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Enhanced user authentication and role-based access control
- [ ] Advanced threat detection algorithms
- [ ] Integration with external security tools
- [ ] Mobile-responsive dashboard improvements
- [ ] Automated alerting via email/SMS
- [ ] Historical data storage and analytics
- [ ] Plugin system for extensibility
