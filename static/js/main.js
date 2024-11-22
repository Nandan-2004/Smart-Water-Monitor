document.addEventListener('DOMContentLoaded', () => {
    // Function to fetch data from the Flask server
    async function fetchData() {
        try {
            // Fetch the data from the Flask endpoint
            const response = await fetch('/get_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse the JSON response
            const data = await response.json();

            if (data.error) {
                console.error("Error from server:", data.error);
                return;
            }

            // Update the DOM with new data
            document.getElementById('timestamp').textContent = data.timestamp || "N/A";
            document.getElementById('flow-rate').textContent = `${data.flow_rate || 0} L/min`;
            document.getElementById('fine').textContent = `${data.fine || 0} Rs`;
            document.getElementById('reward').textContent = `${data.reward || 0} L`;

            // Add new data to the Recent Readings table
            const table = document.getElementById('data-table');
            const newRow = table.insertRow(1); // Insert at the top (after the header row)
            newRow.insertCell(0).textContent = data.timestamp || "N/A";
            newRow.insertCell(1).textContent = `${data.flow_rate || 0} L/min`;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Call fetchData initially and every 5 seconds
    setInterval(fetchData, 5000);
    fetchData(); // Immediate call to populate data on page load
});
