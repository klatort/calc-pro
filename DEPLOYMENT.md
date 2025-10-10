# Deployment Guide - Calc-Pro

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone repository)

### Standard Deployment

1. **Clone and prepare**
```bash
git clone <repository-url>
cd calc-pro
cp .env.example .env
```

2. **Configure environment variables**
Edit `.env` file with your specific values:
```env
# Backend Configuration
PORT=8000
WORKERS=4
LOG_LEVEL=info

# Frontend Configuration  
NGINX_PORT=80
```

3. **Deploy**
```bash
docker-compose up -d --build
```

4. **Verify**
- Frontend: http://localhost (or your server IP)
- Backend API: http://localhost:8000

## Advanced Deployment Scenarios

### Scenario 1: Different Ports

If ports 80 or 8000 are in use:

```env
PORT=8001
NGINX_PORT=8080
```

Then access:
- Frontend: http://localhost:8080
- Backend: http://localhost:8001

### Scenario 2: Production Server with Custom Domain

```env
PORT=8000
WORKERS=8
LOG_LEVEL=warning
BACKEND_URL=http://api.yourdomain.com:8000
NGINX_PORT=80
```

### Scenario 3: Behind Reverse Proxy

If you have nginx/traefik in front:

```env
PORT=8000
NGINX_PORT=3000
BACKEND_URL=http://calc-backend:8000
```

### Scenario 4: Custom Data Files Location

If your price data files are in a different location:

```bash
docker run -d \
  -e WINDOWS_PRICES_DIR=/custom/path/windows_prices.xlsx \
  -e LINUX_PRICES_DIR=/custom/path/linux_prices.xlsx \
  -v /host/custom/path:/custom/path \
  calc-pro-backend
```

## Environment Variables Reference

### Backend Variables

```bash
# Server Configuration
PORT=8000                    # Port for Flask/Gunicorn server
WORKERS=4                    # Number of Gunicorn worker processes
LOG_LEVEL=info              # Logging level: debug|info|warning|error|critical

# File Paths
UPLOAD_FOLDER=/app/uploads                           # Temporary upload directory
WINDOWS_PRICES_DIR=/app/data/windows_prices.xlsx    # Windows pricing data
LINUX_PRICES_DIR=/app/data/RI_linux_prices.xlsx     # Linux pricing data
```

### Frontend Variables

```bash
# Nginx Configuration
NGINX_PORT=80               # Port for Nginx server

# Backend Connection
BACKEND_URL=http://localhost:8000    # URL of the backend API
```

## Monitoring and Maintenance

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart backend
```

### Update After Code Changes
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

## Troubleshooting

### Backend Issues

**Problem**: Backend not accessible
```bash
# Check if container is running
docker ps | grep backend

# Check logs
docker-compose logs backend

# Verify environment variables
docker exec calc-pro-backend env | grep PORT
```

**Problem**: File not found errors
```bash
# Check data files exist
docker exec calc-pro-backend ls -la /app/data/

# Verify volume mounts
docker inspect calc-pro-backend | grep Mounts -A 10
```

### Frontend Issues

**Problem**: Cannot connect to backend
```bash
# Check nginx configuration
docker exec calc-pro-frontend cat /etc/nginx/conf.d/default.conf

# Verify BACKEND_URL was substituted correctly
docker exec calc-pro-frontend env | grep BACKEND_URL
```

**Problem**: 502 Bad Gateway
- Ensure backend is running: `docker-compose ps`
- Check backend health: `curl http://localhost:8000/test/test`
- Verify network connectivity between containers

### Common Issues

**Port Already in Use**
```bash
# Find process using port
sudo lsof -i :8000

# Change port in .env file
PORT=8001
```

**Permission Denied on Uploads**
```bash
# Fix upload folder permissions
docker exec calc-pro-backend chmod 777 /app/uploads
```

## Security Best Practices

1. **Environment Files**
   - Never commit `.env` to version control
   - Use `.env.example` as template
   - Restrict file permissions: `chmod 600 .env`

2. **Production Configuration**
   - Change LOG_LEVEL to `warning` or `error`
   - Use appropriate number of WORKERS (2-4 per CPU core)
   - Enable HTTPS with reverse proxy

3. **Network Security**
   - Use Docker networks for container communication
   - Only expose necessary ports
   - Consider firewall rules for production

## Performance Tuning

### Backend Optimization

```env
# For 4 CPU cores
WORKERS=16

# For production
LOG_LEVEL=warning
```

### Frontend Optimization

- Use CDN for static assets
- Enable gzip compression in Nginx
- Implement caching headers

## Backup and Recovery

### Backup Important Data
```bash
# Backup data files
docker cp calc-pro-backend:/app/data ./backup/

# Backup uploads
docker volume inspect calc-pro_backend-uploads
```

### Restore Data
```bash
# Restore to container
docker cp ./backup/data calc-pro-backend:/app/
```

## Scaling

### Horizontal Scaling

Use docker-compose scale or Kubernetes for multiple instances:

```bash
docker-compose up -d --scale backend=3
```

Add load balancer configuration in `docker-compose.yml`.

### Vertical Scaling

Adjust worker count:
```env
WORKERS=16  # Increase for more concurrent requests
```

---

For more information, see the main [README.md](README.md)
