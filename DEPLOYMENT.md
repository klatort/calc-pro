# Docker Deployment Guide

This guide explains how to build and deploy the calc-pro application using Docker with environment variables for maximum flexibility.

## Quick Start with Docker Compose

1. **Create environment file** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your custom values
   ```

2. **Build and run**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000

## Building Individual Images

### Backend

```bash
# Build the image
docker build -t calc-pro-backend:latest ./backend

# Run with default environment variables
docker run -p 8000:8000 calc-pro-backend:latest

# Run with custom environment variables
docker run -p 9000:9000 \
  -e API_PORT=9000 \
  -e GUNICORN_WORKERS=8 \
  -e UPLOAD_FOLDER=/app/uploads \
  -e WINDOWS_PRICES_DIR=/app/data/windows_prices.xlsx \
  -e LINUX_PRICES_DIR=/app/data/RI_linux_prices.xlsx \
  calc-pro-backend:latest
```

### Frontend

```bash
# Build the image (requires Angular build first)
cd frontend
npm install
npm run build
cd ..
docker build -t calc-pro-frontend:latest ./frontend

# Run with default environment variables
docker run -p 80:80 calc-pro-frontend:latest

# Run with custom backend URL
docker run -p 8080:80 \
  -e BACKEND_URL=http://your-backend-server:8000 \
  calc-pro-frontend:latest
```

## Environment Variables

### Backend Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | `8000` | Port on which the API server listens |
| `GUNICORN_WORKERS` | `4` | Number of Gunicorn worker processes |
| `UPLOAD_FOLDER` | `/app/uploads` | Directory for uploaded files |
| `WINDOWS_PRICES_DIR` | `/app/data/windows_prices.xlsx` | Path to Windows prices file |
| `LINUX_PRICES_DIR` | `/app/data/RI_linux_prices.xlsx` | Path to Linux prices file |

### Frontend Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://localhost:8000` | URL of the backend API server |

### Docker Compose Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FRONTEND_PORT` | `80` | Port to expose for frontend |
| All backend variables | - | Same as backend variables above |

## Pushing to Container Registry

### Docker Hub

```bash
# Login
docker login

# Tag images
docker tag calc-pro-backend:latest yourusername/calc-pro-backend:latest
docker tag calc-pro-frontend:latest yourusername/calc-pro-frontend:latest

# Push images
docker push yourusername/calc-pro-backend:latest
docker push yourusername/calc-pro-frontend:latest
```

### Using Pushed Images

Once images are pushed to a registry, you can deploy anywhere:

```bash
# Pull and run backend
docker pull yourusername/calc-pro-backend:latest
docker run -p 8000:8000 \
  -e API_PORT=8000 \
  yourusername/calc-pro-backend:latest

# Pull and run frontend
docker pull yourusername/calc-pro-frontend:latest
docker run -p 80:80 \
  -e BACKEND_URL=http://your-backend-ip:8000 \
  yourusername/calc-pro-frontend:latest
```

## Production Deployment Example

Create a `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  frontend:
    image: yourusername/calc-pro-frontend:latest
    environment:
      - BACKEND_URL=http://backend:8000
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    image: yourusername/calc-pro-backend:latest
    environment:
      - API_PORT=8000
      - GUNICORN_WORKERS=8
      - UPLOAD_FOLDER=/app/uploads
    ports:
      - "8000:8000"
    volumes:
      - backend-uploads:/app/uploads
      - backend-data:/app/data
    restart: unless-stopped

volumes:
  backend-uploads:
  backend-data:
```

Deploy with:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Backend Issues

**Error: "Failed to find attribute 'app' in 'app'"**

This usually means the Flask app module isn't found. The Dockerfile has been configured to properly expose the app module.

**Permission Issues**

Ensure the upload directory has proper permissions:
```bash
docker exec -it backend chmod -R 777 /app/uploads
```

### Frontend Issues

**Error: "Permission denied" for nginx config**

The Dockerfile now includes proper permission fixes for the nginx user.

**Backend proxy not working**

Ensure the `BACKEND_URL` environment variable is set correctly:
```bash
docker run -e BACKEND_URL=http://backend:8000 calc-pro-frontend:latest
```

## Data Persistence

Backend uploads and data are persisted using Docker volumes. To back up:

```bash
# Backup uploads
docker run --rm -v calc-pro_backend-uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads-backup.tar.gz /data

# Backup data
docker run --rm -v calc-pro_backend-data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz /data
```

To restore:

```bash
# Restore uploads
docker run --rm -v calc-pro_backend-uploads:/data -v $(pwd):/backup alpine tar xzf /backup/uploads-backup.tar.gz -C /

# Restore data
docker run --rm -v calc-pro_backend-data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /
```
