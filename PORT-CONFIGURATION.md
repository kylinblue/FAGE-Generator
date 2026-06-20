# Port Configuration Guide - FAGE Character Generator

This guide explains all port configuration options for local development and Docker deployment.

---

## Quick Reference

| Setup | Frontend | Backend | Use Case |
|-------|----------|---------|----------|
| **Local Dev (Manual)** | 5173 | 8000 | Development with hot reload |
| **Docker Combined** | 8000 | 8000 | Production (frontend served by backend) |
| **Docker Separate (Dev)** | 5173 | 8000 | Docker development environment |
| **Docker Separate (Prod)** | 3000 | 8000 | Production with Nginx frontend |

---

## Option 1: Local Development (Separate Ports) ✅ RECOMMENDED FOR DEVELOPMENT

Run frontend and backend separately for the best development experience.

### Setup

**Terminal 1 - Backend (Port 8000):**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend (Port 5173):**
```bash
cd frontend
npm run dev
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### How It Works

1. Vite dev server runs on port 5173
2. Frontend makes API calls to http://localhost:8000 (configured in `.env.development`)
3. Backend CORS allows requests from localhost:5173
4. Hot reload works for both frontend and backend

### Configuration Files

**Frontend**: `frontend/.env.development`
```bash
VITE_API_URL=http://localhost:8000
```

**Backend**: `backend/config.py`
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:5173",  # Vite dev server
    # ... other origins
]
```

**Frontend**: `frontend/vite.config.js` (already updated)
```javascript
export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
```

---

## Option 2: Docker Combined (Single Port) - Current Default

Frontend and backend both served from port 8000 (production setup).

### Setup

```bash
docker-compose up --build
```

### Access Points

- **Everything**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### How It Works

1. Dockerfile builds frontend (Stage 1)
2. Frontend build copied to backend container
3. FastAPI serves static files from `frontend/dist`
4. All traffic goes through port 8000

### Use Case

- Production deployments
- Simple single-container setup
- When you don't need separate frontend/backend

---

## Option 3: Docker Separate Ports (Development)

Frontend on 5173, backend on 8000, both in Docker with hot reload.

### Setup

```bash
# Use development docker-compose
docker-compose -f docker-compose.dev.yml up --build
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### How It Works

1. Backend container runs on port 8000 with `--reload`
2. Frontend container runs Vite dev server on port 5173
3. Both containers share a network
4. Source code mounted as volumes for hot reload

### Configuration

**File**: `docker-compose.dev.yml` (already created)

### Use Case

- Docker-based development
- Team members without local Python/Node setup
- Consistent development environment

---

## Option 4: Docker Separate Ports (Production with Nginx)

Frontend on 3000 (Nginx), backend on 8000, optimized for production.

### Setup

```bash
# First, build the frontend
cd frontend
npm run build

# Then start with production compose file
docker-compose -f docker-compose.prod-separate.yml up --build
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### How It Works

1. Frontend built into static files
2. Nginx serves static files on port 3000
3. Backend API runs on port 8000
4. Nginx has optimized caching and compression

### Configuration

**File**: `docker-compose.prod-separate.yml` (already created)
**Nginx Config**: `nginx.conf` (already created)

### Use Case

- Production deployments with CDN
- When you want to scale frontend/backend separately
- Static asset caching and optimization

---

## Changing Ports

### Change Frontend Port (Local Dev)

**Edit**: `frontend/vite.config.js`
```javascript
server: {
  port: 3000,  // Change from 5173 to 3000
}
```

Then update CORS in backend:
**Edit**: `backend/config.py`
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",  # Updated port
]
```

### Change Backend Port (Local Dev)

**Edit**: `backend/config.py`
```python
PORT: int = 9000  # Change from 8000
```

Or set environment variable:
```bash
PORT=9000 python main.py
```

Then update frontend:
**Edit**: `frontend/.env.development`
```bash
VITE_API_URL=http://localhost:9000
```

### Change Docker Ports

**Edit**: `docker-compose.yml`
```yaml
services:
  fage-generator:
    ports:
      - "3000:8000"  # Map host:container
```

This makes the app available at http://localhost:3000 (while container uses 8000 internally).

---

## Troubleshooting

### Port Already in Use

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

### CORS Errors

If you change ports and get CORS errors:

1. **Update backend CORS** in `backend/config.py`:
   ```python
   CORS_ORIGINS: List[str] = [
       "http://localhost:YOUR_FRONTEND_PORT",
   ]
   ```

2. **Restart backend** to apply changes

3. **Clear browser cache** and hard reload (Ctrl+Shift+R)

### Frontend Can't Connect to Backend

1. **Check backend is running**: http://localhost:8000/health
2. **Check frontend API URL** in `.env.development`
3. **Check browser console** for error messages
4. **Verify CORS settings** in backend config

### Docker Port Mapping Not Working

1. **Check container is running**: `docker ps`
2. **Check port binding**: `docker port fage-character-generator`
3. **Stop conflicting containers**: `docker stop $(docker ps -q)`
4. **Restart Docker Desktop**

---

## Production Deployment Recommendations

### For Small Apps (< 1000 users)

**Use Option 2**: Docker Combined (Single Port)
- Simpler deployment
- Fewer moving parts
- Lower resource usage

### For Larger Apps (> 1000 users)

**Use Option 4**: Docker Separate (Nginx)
- Better caching
- Can use CDN for frontend
- Independent scaling
- Better performance

---

## Environment Variable Summary

### Frontend Environment Variables

**File**: `frontend/.env.development` (development)
```bash
VITE_API_URL=http://localhost:8000
```

**File**: `frontend/.env.production` (production)
```bash
VITE_API_URL=https://api.yourdomain.com
```

### Backend Environment Variables

**File**: `backend/.env` or `docker-compose.yml`
```bash
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
LOG_LEVEL=INFO
```

---

## Summary

### For Development: Use Option 1
```bash
# Terminal 1
cd backend && venv\Scripts\activate && python main.py

# Terminal 2
cd frontend && npm run dev
```

**Access**: Frontend at http://localhost:5173

### For Production: Use Option 2 (Combined)
```bash
docker-compose up --build
```

**Access**: Everything at http://localhost:8000

### For Advanced Production: Use Option 4 (Nginx)
```bash
docker-compose -f docker-compose.prod-separate.yml up --build
```

**Access**: Frontend at http://localhost:3000, API at http://localhost:8000

---

**Questions?** Check [README.md](README.md) or [DEVELOPMENT.md](DEVELOPMENT.md)
