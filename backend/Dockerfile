# ─────────────────────────────
# 1) Build stage: install deps
# ─────────────────────────────
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for building wheels (psycopg, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy lock/manifest first to leverage Docker layer caching
# Use requirements.txt if you have it; fall back to pyproject if not.
COPY requirements.txt ./
# If you prefer uv/poetry, replace this block accordingly.

# Build wheels into /wheels for a clean runtime image
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ─────────────────────────────
# 2) Runtime stage
# ─────────────────────────────
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Runtime libs only (no compilers)
# libpq5 is required at runtime by psycopg built in the builder stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -ms /bin/bash appuser
WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project files
# (alembic, app/, main.py, config, etc.)
COPY . /app

# Switch to non-root
USER appuser

EXPOSE 8000

# Healthcheck (optional) — expects your /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD ["python","-c","import sys,urllib.request; url='http://127.0.0.1:8000/health'; \
r=0; \
try:\n    resp=urllib.request.urlopen(url,timeout=3); r=0 if resp.status==200 else 1\nexcept Exception:\n    r=1\n; sys.exit(r)"]


# Start the API
# You already bind host/port in __main__; here we run via uvicorn directly.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
