# Multi-stage Dockerfile for FAGE Character Generator
# Stage 1: Build Frontend (Vue.js)
# Stage 2: Setup Backend (Python FastAPI)
# Stage 3: Production Image

# =============================================================================
# Stage 1: Build Frontend
# =============================================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --production=false

# Copy source code
COPY frontend/ ./

# Build for production
RUN npm run build

# =============================================================================
# Stage 2: Setup Backend Dependencies
# =============================================================================
FROM python:3.11-slim AS backend-deps

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 3: Production Image
# =============================================================================
FROM python:3.11-slim AS production

WORKDIR /app

# Copy Python dependencies from backend-deps stage
COPY --from=backend-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-deps /usr/local/bin /usr/local/bin

# Copy backend application
COPY backend/ ./backend/

# Copy frontend build from frontend-builder stage
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p backend/storage/characters backend/generated_pdfs

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Set working directory to backend
WORKDIR /app/backend

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
