import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import { TriageProvider } from './context/TriageContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <TriageProvider>
        <App />
      </TriageProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
