# VAT CRM System

A full-stack VAT CRM application with Flask backend and React/Vite frontend, containerized with Docker.

## Features

- VAT number validation using VIES service
- Company information storage
- Professional UI with 3-step form
- Robust error handling

## Recent Fixes

### VIES Date Parsing Fix

We've added robust date parsing to handle ISO8601 timezone formats in the VIES response. The issue was with the format `2025-07-08+02:00` which was causing errors with the isodate library. We now use a custom parsing function to handle various date formats returned by the VIES service.

## Setup

### Quick Start (Run Backend & Frontend Together)

```bash
# Windows PowerShell
.\start-app.ps1

# Linux/Mac
./start-app.sh
```

This will start both the backend and frontend in separate terminal windows.

### Using Docker Compose

```bash
# Start the application with Docker Compose
docker-compose up -d

# To stop the application
docker-compose down
```

### Manual Setup (Running Components Separately)

#### Backend

```bash
# Install dependencies
cd backend
pip install -r requirements.txt
cd ..

# Run the application (Windows PowerShell)
$env:FLASK_APP = "backend.app:create_app"
$env:FLASK_ENV = "development" 
flask run --host=0.0.0.0 --port=8000

# Alternative: Use the provided script
./run.ps1  # Windows PowerShell
# or
# ./run.sh  # Linux/Mac
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

The backend provides the following API endpoints:

- `GET /`: API documentation
- `GET /api/companies`: List all companies
- `GET /api/companies/<id>`: Get a specific company
- `POST /api/companies/full-check`: Validate a VAT number and store the company information
