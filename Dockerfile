# =============================================================
# VisionStream Dockerfile
# =============================================================
# Multi-stage build:
#   Stage 1 (builder) — install all Python dependencies
#   Stage 2 (runtime) — copy only what's needed, run as non-root
#
# 📌 Lesson 5 Task:
#   - Complete Stage 1:
#       FROM python:3.11-slim AS builder
#       WORKDIR /build
#       COPY requirements.txt .
#       RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
#
#   - Complete Stage 2:
#       FROM python:3.11-slim
#       COPY --from=builder /install /usr/local
#       WORKDIR /app
#       COPY app/ ./app/
#       EXPOSE 8000
#       Create a non-root user and switch to it (security best practice)
#       CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#
#   Build and test:
#       docker build -t visionstream .
#       docker run -p 8000:8000 --env-file .env visionstream
# =============================================================

# TODO (Lesson 5): Stage 1 — Dependency builder
# FROM python:3.11-slim AS builder
# ...

# TODO (Lesson 5): Stage 2 — Runtime image
# FROM python:3.11-slim
# ...
