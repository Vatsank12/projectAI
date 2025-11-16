# VigilantAI - Deployment Guide

## 🚀 Quick Start (Development)

### Windows
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Linux/macOS
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Access:** http://localhost:8000

---

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t vigilantai .
docker run -p 8000:8000 vigilantai
```

### Docker Compose (With Nginx)
```bash
docker-compose up -d
```

**Access:** http://localhost

---

## ☁️ Production Deployment

### Prerequisites
- Python 3.8+
- Nginx
- Systemd (Linux) or Task Scheduler (Windows)

### 1. Setup Server

```bash
# Clone repository
git clone <repo> vigilantai
cd vigilantai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install gunicorn
```

### 2. Environment Configuration

Create `.env` file:
```env
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
```

### 3. Nginx Reverse Proxy

Copy `nginx.conf` to `/etc/nginx/nginx.conf` (or include it):

```nginx
upstream vigilantai {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://vigilantai;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

### 4. Systemd Service (Linux)

Create `/etc/systemd/system/vigilantai.service`:

```ini
[Unit]
Description=VigilantAI Dashboard
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/user/vigilantai
Environment="PATH=/home/user/vigilantai/venv/bin"
ExecStart=/home/user/vigilantai/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8000 \
    --timeout 120 \
    backend.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vigilantai
sudo systemctl start vigilantai
sudo systemctl status vigilantai
```

### 5. SSL/TLS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Update Nginx config:
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
}
```

---

## 📊 Monitoring

### Check Status
```bash
# Docker
docker ps | grep vigilantai

# Systemd
sudo systemctl status vigilantai

# Logs
sudo journalctl -u vigilantai -f
```

### Health Check
```bash
curl http://localhost:8000/health
curl http://localhost:8000/info
```

---

## 🔐 Security Checklist

- [ ] Change default credentials (admin/admin) in production
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Regular backups of database
- [ ] Update dependencies regularly
- [ ] Enable authentication tokens
- [ ] Rate limiting on API endpoints
- [ ] CORS configuration for specific domains
- [ ] Regular security audits

---

## 📈 Performance Optimization

### 1. Database
```bash
sqlite3 backend/vigilant_ai.db ".indices"
```

### 2. Caching
```python
# Add Redis for caching
pip install redis
```

### 3. Load Balancing
```nginx
upstream vigilantai {
    server 127.0.0.1:8000 weight=1;
    server 127.0.0.1:8001 weight=1;
}
```

### 4. Resource Limits
```bash
# Linux
ulimit -n 65536
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Import Errors
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Permission Denied
```bash
chmod +x backend/main.py
sudo chown -R www-data:www-data /path/to/vigilantai
```

### Static Files Not Loading
```bash
# Check frontend directory
ls -la frontend/
ls -la frontend/js/
```

---

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `nginx.conf` | Web server config |
| `docker-compose.yml` | Container orchestration |
| `Dockerfile` | Container image |
| `backend/config.py` | Application config |

---

## 🔄 Backup & Recovery

### Backup Database
```bash
cp backend/vigilant_ai.db backend/vigilant_ai.db.backup
```

### Backup Entire Application
```bash
tar -czf vigilantai-backup.tar.gz vigilantai/
```

### Restore
```bash
tar -xzf vigilantai-backup.tar.gz
```

---

## 🌐 Domain Setup

### DNS Configuration
```
A record: @ -> your-server-ip
CNAME: www -> @
```

### SSL Renewal
```bash
sudo certbot renew --dry-run
```

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Guide](https://gunicorn.org/)

---

## 🆘 Support

- Check logs: `sudo journalctl -u vigilantai -f`
- API Docs: `/docs`
- Health: `/health`
- Info: `/info`

---

**Last Updated:** January 2024
**Version:** 1.0.0
