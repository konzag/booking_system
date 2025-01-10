
export function loadDashboard() {
    console.log("Initializing Room Reservation Dashboard...");
    fetch('/api/dashboard')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
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
                        console.log(`Reservation found: ${reservationKey}`);
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
            console.error("Error loading dashboard:", error);
            alert("Failed to load dashboard data.");
        });
}
