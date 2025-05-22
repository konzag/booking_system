
import { fetchData } from './frontend_utils.js';

export function loadDashboard() {
    console.log("Initializing Room Reservation Dashboard...");
    fetchData('/api/dashboard')
        .then(data => {
            console.log("Dashboard Data:", data);

            const dashboard = document.getElementById('dashboard');
            dashboard.innerHTML = '<h1>Πίνακας Κρατήσεων Δωματίων</h1>';

            const table = document.createElement('table');
            const headerRow = table.insertRow();

            const emptyCell = headerRow.insertCell();
            emptyCell.innerText = 'Δωμάτια/Ημερομηνίες';

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
                        cell.innerHTML = `<strong>${reservation.name}</strong><br>${reservation.phone}`;
                        cell.style.backgroundColor = '#ffe6e6';
                        console.log(`Reservation found: Room=${room}, Date=${date}, Reservation=${reservationKey}`);
                    } else {
                        const btn = document.createElement('button');
                        btn.innerText = 'Ελεύθερο';
                        btn.onclick = () => console.log(`Clicked on empty cell: Room=${room}, Date=${date}`);
                        cell.appendChild(btn);
                    }
                });
            });

            dashboard.appendChild(table);
        })
        .catch(error => {
            console.error("Error loading dashboard:", error);
            alert("Failed to load dashboard data. Please check the console for more details.");
        });
}
