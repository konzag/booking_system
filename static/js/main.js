
import { fetchData } from './frontend_utils.js';

function loadDashboard() {
    fetchData('/api/dashboard')
        .then(data => {
            console.log("Loaded dashboard data:", data);
        })
        .catch(error => {
            console.error("Failed to load dashboard:", error);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
