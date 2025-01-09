
// frontend_reservation.js
import { loadDashboard } from './frontend_dashboard.js';

export async function makeReservation(room, date) {
    const name = prompt("Όνομα και Επίθετο:");
    if (!name) return alert("Reservation cancelled.");

    const phone = prompt("Τηλέφωνο:");
    if (!phone) return alert("Reservation cancelled.");

    const provider = prompt("Κράτηση από (Booking/Τηλεφωνικά):");
    if (!provider) return alert("Reservation cancelled.");

    const nights = prompt("Βραδιές (πλήθος διανυκτερεύσεων):");
    if (!nights || isNaN(nights) || nights <= 0) {
        return alert("Invalid input for nights. Reservation cancelled.");
    }

    fetch("/api/reserve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room, date, name, phone, provider, nights })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(() => {
        alert("Reservation completed successfully!");
        loadDashboard(); // Reload dashboard after reservation
    })
    .catch(error => {
        console.error("Error making reservation:", error);
        alert("An error occurred while making the reservation.");
    });
}
