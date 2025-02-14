async function fetchReservations() {
    console.log("Fetching reservations...");
    const response = await fetch("/api/get_reservations");
    const data = await response.json();
    const tableBody = document.getElementById("reservationBody");

    const rooms = [
        "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)", "ΤΕΤΡΑΚΛΙΝΟ",
        "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ", "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
    ];

    const dates = generateDateRange(currentStartDate, 15);

    let headerRow = "<tr><th>Δωμάτιο</th>";
    dates.forEach(date => {
        headerRow += `<th>${date}</th>`;
    });
    headerRow += "</tr>";
    
    tableBody.innerHTML = headerRow;

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
