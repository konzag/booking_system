
// frontend_dashboard.js
import { makeReservation } from './frontend_reservation.js';

export function loadDashboard() {
    fetch('/api/dashboard')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            const dashboard = document.getElementById('dashboard');
            dashboard.innerHTML = '';

            const table = document.createElement('table');
            const headerRow = table.insertRow();

            const emptyCell = headerRow.insertCell();
            emptyCell.innerText = 'Rooms/Dates';

            data.dates.forEach(date => {
                const dateCell = headerRow.insertCell();
                dateCell.innerText = date;
            });

            data.rooms.forEach(room => {
                const row = table.insertRow();
                const roomCell = row.insertCell();
                roomCell.innerText = room;

                data.dates.forEach(date => {
                    const cell = row.insertCell();
                    const reservationKey = `${room}-${date}`;
                    const reservation = data.reservations[reservationKey];

                    if (reservation) {
                        cell.innerHTML = `<strong style="color: red;">${reservation.name}</strong><br><span style="color: red;">${reservation.provider}</span>`;
                        cell.style.backgroundColor = '#ffe6e6';
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
        .catch(error => console.error("Error loading dashboard:", error));
}
