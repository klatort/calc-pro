# Migration Guide: Hardcoded Values to Environment Variables

This document describes the changes made to support environment variables instead of hardcoded values.

## What Changed

### Backend Changes

#### 1. `backend/config.py`
**Before:**
```python
UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')
WINDOWS_PRICES_DIR = os.path.join(ROOT, './data/windows_prices.xlsx')
LINUX_PRICES_DIR = os.path.join(ROOT, './data/RI_linux_prices.xlsx')
```

**After:**
```python
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(ROOT, 'uploads'))
WINDOWS_PRICES_DIR = os.getenv('WINDOWS_PRICES_DIR', os.path.join(ROOT, './data/windows_prices.xlsx'))
LINUX_PRICES_DIR = os.getenv('LINUX_PRICES_DIR', os.path.join(ROOT, './data/RI_linux_prices.xlsx'))
```

#### 2. `backend/dockerfile`
**Before:**
```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--log-level", "debug", "app:app"]
```

**After:**
```dockerfile
ENV API_PORT=8000 \
    GUNICORN_WORKERS=4 \
    UPLOAD_FOLDER=/app/uploads \
    WINDOWS_PRICES_DIR=/app/data/windows_prices.xlsx \
    LINUX_PRICES_DIR=/app/data/RI_linux_prices.xlsx

CMD gunicorn --bind 0.0.0.0:${API_PORT} --workers ${GUNICORN_WORKERS} --log-level debug app:app
```

### Frontend Changes

#### 1. `frontend/default` (Nginx Config)
**Before:**
```nginx
location / {
    proxy_pass http://101.44.10.234:8000/;
```

**After:**
```nginx
location /api/ {
    proxy_pass ${BACKEND_URL}/;
```

**Note:** The location was changed from `/` to `/api/` to avoid conflicts with serving the Angular app.

#### 2. `frontend/dockerfile`
**Before:**
```dockerfile
COPY default /etc/nginx/sites-enabled
CMD ["nginx", "-g", "daemon off;"]
```

**After:**
```dockerfile
COPY default /etc/nginx/templates/default.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh
ENV BACKEND_URL=http://localhost:8000
ENTRYPOINT ["/docker-entrypoint.sh"]
```

#### 3. New File: `frontend/docker-entrypoint.sh`
This script substitutes environment variables into the nginx configuration at runtime.

### Docker Compose Changes

**Before:**
```yaml
services:
  frontend:
    ports:
      - "80:80"
  backend:
    ports:
      - "8000:8000"
```

**After:**
```yaml
services:
  frontend:
    environment:
      - BACKEND_URL=${BACKEND_URL:-http://backend:8000}
    ports:
      - "${FRONTEND_PORT:-80}:80"
  backend:
    environment:
      - API_PORT=${API_PORT:-8000}
      - GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
      # ... more env vars
    ports:
      - "${API_PORT:-8000}:${API_PORT:-8000}"
    volumes:
      - backend-uploads:/app/uploads
      - backend-data:/app/data
```

## Migration Steps for Existing Deployments

### Option 1: Using Default Values (No Changes Required)

If you're happy with the default values, you don't need to do anything. The application will work exactly as before.

### Option 2: Custom Configuration

1. **Create a `.env` file** in the root directory:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** with your custom values:
   ```bash
   API_PORT=9000
   GUNICORN_WORKERS=8
   BACKEND_URL=http://your-custom-backend:9000
   ```

3. **Rebuild and restart**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Option 3: Using Pre-built Images

1. **Pull images from registry**:
   ```bash
   docker pull yourusername/calc-pro-backend:latest
   docker pull yourusername/calc-pro-frontend:latest
   ```

2. **Run with environment variables**:
   ```bash
   # Backend
   docker run -d \
     -p 8000:8000 \
     -e API_PORT=8000 \
     -e GUNICORN_WORKERS=4 \
     --name backend \
     yourusername/calc-pro-backend:latest

   # Frontend
   docker run -d \
     -p 80:80 \
     -e BACKEND_URL=http://backend:8000 \
     --name frontend \
     --link backend:backend \
     yourusername/calc-pro-frontend:latest
   ```

## Breaking Changes

### Frontend API Proxy Path

⚠️ **Important:** The nginx proxy location has been changed from `/` to `/api/` to avoid conflicts.

**If your frontend code makes API calls directly** (without going through the proxy), you may need to update the API endpoints in your Angular code.

Currently, the Angular app uses the `apiUrl` from `environment.ts` files, which should continue to work. The proxy is available for additional flexibility.

## Rollback Instructions

If you need to rollback to the previous configuration:

1. **Checkout previous commit**:
   ```bash
   git checkout HEAD~1
   ```

2. **Rebuild containers**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## Testing the Changes

### Test Backend

```bash
# Build
docker build -t calc-pro-backend:test ./backend

# Run with custom port
docker run -p 9000:9000 -e API_PORT=9000 calc-pro-backend:test

# Test API
curl http://localhost:9000/test/render
```

### Test Frontend

```bash
# Build
docker build -t calc-pro-frontend:test ./frontend

# Run with custom backend URL
docker run -p 8080:80 -e BACKEND_URL=http://host.docker.internal:8000 calc-pro-frontend:test

# Access
open http://localhost:8080
```

### Test Docker Compose

```bash
# Create custom .env
cat > .env << EOF
API_PORT=9000
FRONTEND_PORT=8080
BACKEND_URL=http://backend:9000
EOF

# Run
docker-compose up --build

# Test
curl http://localhost:9000/test/render
open http://localhost:8080
```

## Support

If you encounter any issues during migration, please:

1. Check the [DEPLOYMENT.md](./DEPLOYMENT.md) guide
2. Verify environment variables are set correctly
3. Check Docker logs: `docker-compose logs`
4. Verify nginx configuration was generated: `docker exec frontend cat /etc/nginx/conf.d/default.conf`

## Benefits of This Migration

✅ **Flexibility**: Deploy anywhere without rebuilding images
✅ **Security**: No hardcoded IPs or ports in the codebase
✅ **Scalability**: Easy to adjust worker count and other settings
✅ **Portability**: Same image works in dev, staging, and production
✅ **Best Practices**: Follows 12-factor app methodology
