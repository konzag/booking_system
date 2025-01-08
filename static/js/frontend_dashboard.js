
// frontend_dashboard.js
import { makeReservation } from './frontend_reservation.js';

export function loadDashboard() {
    fetch('/api/dashboard')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Dashboard Data:', data);
            const dashboard = document.getElementById('dashboard');
            dashboard.innerHTML = '';

            const table = document.createElement('table');
            const headerRow = table.insertRow();

            // Dates Header
            const emptyCell = headerRow.insertCell();
            emptyCell.innerText = 'Rooms/Dates';

            data.dates.forEach(date => {
                const dateCell = headerRow.insertCell();
                dateCell.innerText = date;
            });

            // Rooms and Reservations
            data.rooms.forEach(room => {
                const row = table.insertRow();
                const roomCell = row.insertCell();
                roomCell.innerText = room;

                data.dates.forEach(date => {
                    const cell = row.insertCell();
                    const reservation = data.reservations[`${room}-${date}`];

                    if (reservation) {
                        cell.innerText = `${reservation.name}
${reservation.phone}`;
                        cell.style.backgroundColor = '#f8d7da';
                        cell.onclick = () => editReservation(room, date);
                    } else {
                        const btn = document.createElement('button');
                        btn.innerText = 'Ελεύθερο';
                        btn.onclick = () => makeReservation(room, date);
                        cell.appendChild(btn);
                    }
                });
            });

            dashboard.appendChild(table);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            document.getElementById('dashboard').innerHTML = '<p style="color: red;">Failed to load dashboard data.</p>';
        });
}
