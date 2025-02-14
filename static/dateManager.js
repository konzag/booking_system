let currentStartDate = new Date();

function formatDate(date) {
    return date.toLocaleDateString('el-GR', { day: '2-digit', month: '2-digit', year: '2-digit' });
}

function generateDateRange(startDate, days = 15) {
    let dates = [];
    for (let i = 0; i < days; i++) {
        let date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        dates.push(formatDate(date));
    }
    return dates;
}

function updateDateRange(newStartDate) {
    currentStartDate = new Date(newStartDate);
    fetchReservations();
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("prevDates").addEventListener("click", function () {
        let newStartDate = new Date(currentStartDate);
        newStartDate.setDate(currentStartDate.getDate() - 15);
        updateDateRange(newStartDate);
    });

    document.getElementById("nextDates").addEventListener("click", function () {
        let newStartDate = new Date(currentStartDate);
        newStartDate.setDate(currentStartDate.getDate() + 15);
        updateDateRange(newStartDate);
    });

    document.getElementById("today").addEventListener("click", function () {
        updateDateRange(new Date());
    });
});
