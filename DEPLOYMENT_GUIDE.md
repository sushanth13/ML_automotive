# Deployment Guide

This guide covers deploying the FastAPI application to a production environment.

## Prerequisites
- A Linux server (Ubuntu/Debian recommended)
- Python 3.9+ installed
- Nginx or Apache (for reverse proxy)

## Steps
1. **Clone the repository/copy files** to your server.
2. **Create a Virtual Environment**:
   `python -m venv venv`
   `source venv/bin/activate`
3. **Install Dependencies**:
   `pip install -r requirements.txt`
4. **Run with Gunicorn/Uvicorn**:
   In production, do not use `--reload`. Instead, use gunicorn with Uvicorn workers:
   `pip install gunicorn`
   `gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000`
5. **Set up Nginx**:
   Configure Nginx to proxy pass requests from port 80/443 to `localhost:8000`.

## Security
Ensure your `.pkl` model file is kept secure and not exposed to the public internet except through the `/predict` API endpoint.
