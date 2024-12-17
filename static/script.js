
const roomNames = [
    "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)",
    "ΤΕΤΡΑΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ",
    "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
];

let currentStartDate = 1;

function loadDashboard() {
    const startDay = currentStartDate;
    const endDay = startDay + 14;
    const days = Array.from({ length: 15 }, (_, i) => startDay + i);

    fetch(`/api/bookings?start=${formatDate(startDay)}&end=${formatDate(endDay)}`)
        .then(response => response.json())
        .then(data => {
            const dashboard = document.getElementById('dashboard');
            let tableHTML = '<table><thead><tr><th>Δωμάτιο</th>';

            days.forEach(day => {
                tableHTML += `<th>${formatDate(day)}</th>`;
            });

            tableHTML += '</tr></thead><tbody>';

            roomNames.forEach((room, roomIndex) => {
                tableHTML += `<tr><td>${room}</td>`;
                days.forEach(day => {
                    const booking = data.find(
                        b =>
                            b.room === room &&
                            new Date(`${new Date().getFullYear()}-${b.check_in.split('/').reverse().join('-')}`) <=
                                new Date(`${new Date().getFullYear()}-${formatDate(day).split('/').reverse().join('-')}`) &&
                            new Date(`${new Date().getFullYear()}-${b.check_out.split('/').reverse().join('-')}`) >=
                                new Date(`${new Date().getFullYear()}-${formatDate(day).split('/').reverse().join('-')}`)
                    );
                    tableHTML += `<td>${
                        booking
                            ? `<div class="dropdown">
                                <button onclick="toggleDropdown(${booking.id})">${booking.name}</button>
                                <div id="dropdown-${booking.id}" class="dropdown-content">
                                    <button onclick="editBooking(${booking.id})">Επεξεργασία</button>
                                    <button onclick="deleteBooking(${booking.id})">Διαγραφή</button>
                                </div>
                               </div>`
                            : `<button onclick="addBooking('${room}', '${formatDate(day)}')">Κράτηση</button>`
                    }</td>`;
                });
                tableHTML += '</tr>';
            });

            tableHTML += '</tbody></table>';
            dashboard.innerHTML = tableHTML;
        })
        .catch(error => console.error('Error loading dashboard:', error));
}

function formatDate(day) {
    const month = new Date().getMonth() + 1;
    return `${String(day).padStart(2, '0')}/${String(month).padStart(2, '0')}`;
}

function toggleDropdown(id) {
    const dropdown = document.getElementById(`dropdown-${id}`);
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function addBooking(room, checkInDate) {
    const name = prompt('Όνομα:');
    const phone = prompt('Τηλέφωνο:');
    const nights = parseInt(prompt('Διανυκτερεύσεις:'), 10);
    const source = confirm('Booking ή Τηλέφωνο; Πατήστε OK για Booking ή Cancel για Τηλέφωνο') ? 'Booking' : 'Τηλέφωνο';

    fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            room,
            name,
            phone,
            check_in: checkInDate,
            check_out: formatDate(parseInt(checkInDate.split('/')[0], 10) + nights - 1),
            source
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Η κράτηση ολοκληρώθηκε επιτυχώς!');
            loadDashboard(); // Reload dashboard to reflect new booking
        } else {
            response.json().then(data => alert(data.message));
        }
    })
    .catch(error => console.error('Error adding booking:', error));
}

function editBooking(id) {
    const newName = prompt('Νέο Όνομα:');
    const newPhone = prompt('Νέο Τηλέφωνο:');
    const newNights = parseInt(prompt('Νέες Διανυκτερεύσεις:'), 10);
    const newCheckOut = formatDate(parseInt(checkInDate.split('/')[0], 10) + newNights - 1);

    fetch('/api/bookings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, name: newName, phone: newPhone, check_in: checkInDate, check_out: newCheckOut, source: 'Updated' })
    })
    .then(response => {
        if (response.ok) {
            alert('Η κράτηση ενημερώθηκε!');
            loadDashboard();
        } else {
            alert('Πρόβλημα κατά την ενημέρωση!');
        }
    })
    .catch(error => console.error('Error updating booking:', error));
}

function deleteBooking(id) {
    if (confirm('Είστε σίγουρος ότι θέλετε να διαγράψετε αυτή την κράτηση;')) {
        fetch('/api/bookings', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        })
        .then(response => {
            if (response.ok) {
                alert('Η κράτηση διαγράφηκε!');
                loadDashboard();
            } else {
                alert('Πρόβλημα κατά τη διαγραφή!');
            }
        })
        .catch(error => console.error('Error deleting booking:', error));
    }
}

function deleteAllBookings() {
    if (confirm('Είστε σίγουρος ότι θέλετε να διαγράψετε όλες τις κρατήσεις αυτού του μήνα;')) {
        const startDay = currentStartDate;
        const endDay = startDay + 14;

        fetch(`/api/bookings?start=${formatDate(startDay)}&end=${formatDate(endDay)}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert('Όλες οι κρατήσεις διαγράφηκαν!');
                loadDashboard();
            } else {
                alert('Πρόβλημα κατά τη διαγραφή κρατήσεων!');
            }
        })
        .catch(error => console.error('Error deleting all bookings:', error));
    }
}

function previous() {
    if (currentStartDate > 1) {
        currentStartDate -= 15;
        loadDashboard();
    }
}

function next() {
    if (currentStartDate + 15 <= 31) {
        currentStartDate += 15;
        loadDashboard();
    }
}

window.onload = loadDashboard;
