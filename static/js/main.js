
// main.js
import { loadDashboard } from './frontend_dashboard.js';
import { makeReservation } from './frontend_reservation.js';

window.onload = () => {
    console.log("Initializing Dashboard...");
    loadDashboard();
};
