# CRM Celery Setup Guide

This guide explains how to set up and run Celery with Redis for the CRM application's background tasks and scheduled reports.

## Prerequisites

- Python 3.8+
- Django 4.2+
- Redis server

## Installation Steps

### 1. Install Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**Windows:**
Download and install Redis from the official website or use WSL.

### 2. Verify Redis Installation
```bash
redis-cli ping
```
You should receive a `PONG` response.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start Celery Worker
```bash
celery -A crm worker -l info
```

### 6. Start Celery Beat Scheduler
```bash
celery -A crm beat -l info
```

## CRM Setup Instructions

### 1. Install Redis and Python Dependencies

- Install Redis:
  - macOS: `brew install redis`
  - Ubuntu: `sudo apt-get install redis-server`
- Start Redis:
  - macOS: `brew services start redis`
  - Ubuntu: `sudo service redis-server start`
- Install Python dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### 2. Run Migrations

```sh
python manage.py migrate
```

### 3. Start Celery Worker

```sh
celery -A crm worker -l info
```

### 4. Start Celery Beat Scheduler

```sh
celery -A crm beat -l info
```

### 5. Verify CRM Report Logs

- Weekly reports are logged to `/tmp/crm_report_log.txt`.
- Each entry: `YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue`

## Troubleshooting
- Ensure Redis is running before starting Celery.
- Check `/tmp/crm_report_log.txt` for report output.
- For issues with GraphQL queries, verify the endpoint and schema field names.
