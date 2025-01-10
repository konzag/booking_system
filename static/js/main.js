
import { loadDashboard } from './frontend_dashboard.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log("Application started. Initializing dashboard...");
    try {
        loadDashboard();
        console.log("Dashboard initialization complete.");
    } catch (error) {
        console.error("Error initializing dashboard:", error);
    }
});
