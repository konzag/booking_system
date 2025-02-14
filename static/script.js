document.addEventListener("DOMContentLoaded", function () {
    fetchReservations();
});

async function fetchReservations() {
    console.log("Fetching reservations...");
    const response = await fetch("/api/get_reservations");
    const data = await response.json();
    const tableBody = document.getElementById("reservationBody");

    const rooms = [
        "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)", "ΤΕΤΡΑΚΛΙΝΟ",
        "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ", "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
    ];
    
    tableBody.innerHTML = "";
    
    let today = new Date();
    let dates = [];
    for (let i = 0; i < 15; i++) {
        let date = new Date();
        date.setDate(today.getDate() + i);
        dates.push(date.toLocaleDateString('el-GR', { day: '2-digit', month: '2-digit', year: '2-digit' }));
    }
    
    let headerRow = "<tr><th>Δωμάτιο</th>";
    dates.forEach(date => {
        headerRow += `<th>${date}</th>`;
    });
    headerRow += "</tr>";
    
    tableBody.innerHTML += headerRow;
    
    rooms.forEach(room => {
        let row = `<tr><td>${room}</td>`;
        dates.forEach(date => {
            row += `<td class='free-room' style='background-color: lightgreen;' data-room="${room}" data-date="${date}" onclick="openReservationForm('${room}', '${date}')">Ελεύθερο</td>`;
        });
        row += "</tr>";
        tableBody.innerHTML += row;
    });

    console.log("Reservations loaded!");
}
