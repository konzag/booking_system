
// frontend_reservation.js
import { showProviderSelection } from './frontend_utils.js';

export async function makeReservation(room, date) {
    if (!confirm(`You selected Room: ${room} on Date: ${date}. Do you want to continue?`)) {
        alert('Reservation process cancelled.');
        return;
    }

    const name = prompt('Όνομα και Επίθετο:');
    if (!name) {
        alert('Reservation cancelled at Name step.');
        return;
    }

    const phone = prompt('Τηλέφωνο:');
    if (!phone) {
        alert('Reservation cancelled at Phone step.');
        return;
    }

    const provider = await showProviderSelection();
    if (!provider) {
        alert('Reservation cancelled at Provider step.');
        return;
    }

    let nights;
    while (true) {
        nights = prompt('Βραδιές (πλήθος διανυκτερεύσεων):');
        if (!nights || isNaN(nights) || nights <= 0) {
            alert('Invalid nights input. Please enter a valid positive number.');
        } else {
            break;
        }
    }

    fetch('/api/reserve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room, name, phone, provider, arrival_date: date, nights })
    })
    .then(() => {
        alert('Reservation completed successfully!');
        loadDashboard();
    })
    .catch(error => {
        console.error('Error making reservation:', error);
        alert('An error occurred while making the reservation.');
    });
}
