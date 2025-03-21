# Developer Setup Guide

This guide will help you set up the Syntelligence project for local development.

## Prerequisites

- Python 3.13 or higher
- Node.js 20 or higher
- Docker (for containerized deployments)

## Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/syntelligence.git
   cd syntelligence
   ```

2. Create and activate a virtual environment:
   ```bash
   # Using uv (recommended)
   uv venv .venv

   # Activate on Windows
   .venv\Scripts\activate

   # Activate on Unix/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -e ".[dev,docs]"  # Install with development and documentation extras
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Documentation

To build and serve the documentation locally:

```bash
# From the project root
pip install -e "backend/.[docs]"
mkdocs serve
```

The documentation will be available at `http://127.0.0.1:8000/`.
