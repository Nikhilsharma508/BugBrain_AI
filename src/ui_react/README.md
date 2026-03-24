# React (Vite) + FastAPI Bug Triage UI

This directory contains the modernized, high-performance replacement for the legacy Streamlit UI. 

## Structure

- **`api/`**: Contains the FastAPI server and endpoints that wrap the Python orchestration logic.
- **`frontend/`**: Contains the Vite-based React application representing the user interface.

## How to Run locally

You will need two terminal windows to run both the backend API and the frontend concurrently.

## One-Command Startup (Recommended)

From the project root directory, you can now start both the backend and frontend at once:

```bash
npm run dev
```

This will run FastAPI on port 8000 and the React app on port 5173 concurrently.

### Manual Setup (Separate Terminals)

If you prefer to run them separately:

#### 1. Start the FastAPI Backend
```bash
cd src/ui_react/api
# Ensure your virtual environment is activated
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://localhost:8000`.

#### 2. Start the React Frontend
```bash
cd src/ui_react/frontend
npm run dev
```
The Vite server will start on `http://localhost:5173`. Open this URL in your browser to view the application.

## Note on Legacy Streamlit UI
The old Streamlit UI remains available in `src/ui` until validation of this React interface is complete, at which point it will be fully deprecated.
