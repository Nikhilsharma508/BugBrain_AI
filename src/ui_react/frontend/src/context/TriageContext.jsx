import React, { createContext, useContext, useState } from 'react';

const TriageContext = createContext();

export const useTriage = () => {
    return useContext(TriageContext);
};

export const TriageProvider = ({ children }) => {
    const defaultStatus = {
        preprocess: { active: false, complete: false, desc: 'Waiting for input...' },
        extract: { active: false, complete: false, desc: 'Waiting for input...' },
        duplicate_detection: { active: false, complete: false, desc: 'Waiting for input...' },
        triage: { active: false, complete: false, desc: 'Waiting for input...' },
    };

    const [bugTrace, setBugTrace] = useState('');
    const [userReview, setUserReview] = useState('');
    const [isRunning, setIsRunning] = useState(false);
    const [error, setError] = useState('');
    const [status, setStatus] = useState(defaultStatus);
    const [finalResult, setFinalResult] = useState(null);
    const [similarReports, setSimilarReports] = useState([]);
    const [combinedText, setCombinedText] = useState('');

    const value = {
        bugTrace, setBugTrace,
        userReview, setUserReview,
        isRunning, setIsRunning,
        error, setError,
        status, setStatus,
        finalResult, setFinalResult,
        similarReports, setSimilarReports,
        combinedText, setCombinedText,
        defaultStatus
    };

    return (
        <TriageContext.Provider value={value}>
            {children}
        </TriageContext.Provider>
    );
};
