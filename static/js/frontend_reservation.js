
import { loadDashboard } from './frontend_dashboard.js';

export function makeReservation(room, date) {
    console.log(`Initializing reservation wizard for room: ${room} on date: ${date}`);
    
    const formHtml = `
        <div id="reservation-form" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #f9f9f9; padding: 20px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
            <h3>Νέα Κράτηση</h3>
            <label>Όνομα και Επίθετο: <input type="text" id="name" /></label><br /><br />
            <label>Τηλέφωνο: <input type="text" id="phone" /></label><br /><br />
            <label>Κράτηση από: 
                <select id="provider">
                    <option value="Booking">Booking</option>
                    <option value="Τηλεφωνικά">Τηλεφωνικά</option>
                </select>
            </label><br /><br />
            <label>Βραδιές (πλήθος διανυκτερεύσεων): <input type="number" id="nights" min="1" /></label><br /><br />
            <button id="submit-reservation" style="padding: 5px 10px; background: #4caf50; color: white; border: none; border-radius: 4px;">Υποβολή</button>
            <button id="cancel-reservation" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 4px; margin-left: 10px;">Ακύρωση</button>
        </div>
    `;

    const container = document.createElement('div');
    container.innerHTML = formHtml;
    document.body.appendChild(container);

    document.getElementById('submit-reservation').onclick = function () {
        const name = document.getElementById('name').value;
        const phone = document.getElementById('phone').value;
        const provider = document.getElementById('provider').value;
        const nights = document.getElementById('nights').value;

        if (!name || !phone || !provider || !nights) {
            alert("Όλα τα πεδία είναι υποχρεωτικά!");
            return;
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
            alert("Η κράτηση ολοκληρώθηκε με επιτυχία!");
            container.remove(); // Remove form from DOM
            loadDashboard(); // Refresh the dashboard
        })
        .catch(error => {
            console.error("Error making reservation:", error);
            alert("Παρουσιάστηκε σφάλμα κατά τη διαδικασία κράτησης.");
        });
    };

    document.getElementById('cancel-reservation').onclick = function () {
        console.log("Reservation wizard canceled.");
        container.remove(); // Remove the form without making a reservation
    };
}
