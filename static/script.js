async function fetchReservations() {
    const response = await fetch("/api/dashboard");
    const data = await response.json();
    const tableBody = document.getElementById("reservationBody");
    
    const rooms = ["ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)", "ΤΕΤΡΑΚΛΙΝΟ"];
    tableBody.innerHTML = "";
    rooms.forEach(room => {
        let row = `<tr><td>${room}</td>`;
        for (let i = 0; i < 3; i++) {
            row += `<td class='free' onclick='openReservationForm("${room}", ${i})'>Ελεύθερο</td>`;
        }
        row += "</tr>";
        tableBody.innerHTML += row;
    });
}

function openReservationForm(room, dayIndex) {
    alert(`Reserve ${room} on day ${dayIndex + 10}/02/25`);
}

fetchReservations();
