# UI React Migration Guide 🚀

This guide provides a comprehensive overview of the `ui_react` project structure and the purpose of each file. It's designed to help you understand how the React frontend and FastAPI backend work together to replace the legacy Streamlit UI.

## 🏗️ Project Architecture

The project is split into two distinct parts:
1.  **`src/ui_react/api/`**: The Python Backend (FastAPI).
2.  **`src/ui_react/frontend/`**: The React Frontend (Vite).

---

## 🐍 Backend: `src/ui_react/api/`

The backend handles all the heavy lifting: processing bug reports, running the LangGraph pipeline, and fetching data from the vector store.

### 🔑 Core Files
*   **[`app.py`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/api/app.py)**: 
    *   The main entry point for the FastAPI server.
    *   Configures **CORS** (so the React app can talk to it).
    *   Sets the working directory to the project root so that paths like `Data/vector_store` are consistent with the original Streamlit app.
    *   Loads the API routers defined below.
*   **`routers/`**:
    *   **[`triage.py`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/api/routers/triage.py)**: Handles the `/api/triage/run` and `/api/triage/commit` endpoints. It streams the LangGraph pipeline's status updates directly to the frontend.
    *   **[`dashboard.py`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/api/routers/dashboard.py)**: Handles the `/api/dashboard` endpoint, providing historical metrics, severity counts, and team load data for the charts.
*   **`components/result_display.py`**: A helper file (legacy logic) that can be removed once the React frontend is fully verified.

---

## ⚛️ Frontend: `src/ui_react/frontend/`

The frontend is a modern React application built with Vite. It uses **Glassmorphism** styling to provide a premium feel.

### 🔑 Core Files
*   **[`src/main.jsx`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/main.jsx)**: The React entry point. It wraps the app in `BrowserRouter` for routing.
*   **[`src/App.jsx`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/App.jsx)**: Defines the global layout including the `Sidebar` and the main routes.
*   **[`src/index.css`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/index.css)**: **Variable Central.** Contains all CSS tokens for colors, glass effects, gradients, and font settings.
*   **`src/components/`**:
    *   **[`Sidebar.jsx`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/components/Sidebar.jsx)**: The navigation bar on the left.
    *   **[`GlassCard.jsx`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/components/GlassCard.jsx)**: A reusable wrapper component that gives any content that "frosted glass" look.
*   **`src/pages/`**:
    *   **[`TriagePipeline.jsx`](file:///Users/ni ke/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/pages/TriagePipeline.jsx)**: 
        *   Contains the form for submitting bug reports.
        *   Uses `fetch` and a `StreamReader` to process the SSE (Server-Sent Events) from the backend.
        *   Renders the **Final Triage Report**, including Technical Details and Stack Trace.
    *   **[`Dashboard.jsx`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/frontend/src/pages/Dashboard.jsx)**: 
        *   Fetches aggregate data from `/api/dashboard`.
        *   Uses **Recharts** to render animated Bar Charts for Severity Spread and Team Load.

---

## 🔄 How to Modify the UI

1.  **Styling**: To change the theme colors or glass effects, edit **`src/index.css`**.
2.  **Navigation**: To add a new page or link, update **`src/App.jsx`** and **`src/components/Sidebar.jsx`**.
3.  **Pipeline Logic**: To change how the report looks or what data it shows, edit **`src/pages/TriagePipeline.jsx`**.
4.  **Backend Data**: To change what data is sent to the UI, edit the routers in **`src/ui_react/api/routers/`**.

---

## 🚀 Running the Project

Check the main **[`README.md`](file:///Users/nike/Documents/Data%20Science%20Work/Project/uc20_bug_report_summarizer/src/ui_react/README.md)** in the root for the single-command startup instruction (`npm run dev`).
