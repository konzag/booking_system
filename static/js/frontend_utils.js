
// frontend_utils.js
export function showProviderSelection() {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.innerHTML = `
            <h3>Κράτηση από:</h3>
            <select id="providerSelect">
                <option value="Booking">Booking</option>
                <option value="Τηλεφωνικά">Τηλεφωνικά</option>
            </select>
            <button onclick="resolveProvider()">OK</button>`;
        document.body.appendChild(modal);
        window.resolveProvider = () => {
            const provider = document.getElementById('providerSelect').value;
            document.body.removeChild(modal);
            resolve(provider);
        };
    });
}
