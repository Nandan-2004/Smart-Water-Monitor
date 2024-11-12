document.addEventListener('DOMContentLoaded', () => {
    // Define water usage thresholds
    const highUsageThreshold = 80.0;  // Set the high usage threshold
    const lowUsageThreshold = 10.0;   // Set the low usage threshold

    // Store the fine and reward values persistently
    let fine = 0;
    let reward = 0;

    // Track the current month to reset fine and reward at the start of each month
    let currentMonth = new Date().getMonth(); // Get the current month (0-based index)

    // Function to reset fine and reward at the start of a new month
    function resetMonthlyValues() {
        const newMonth = new Date().getMonth();
        if (newMonth !== currentMonth) {
            fine = 0;
            reward = 0;
            currentMonth = newMonth; // Update the current month
            console.log("New month started! Fine and reward values reset.");
        }
    }

    // Function to fetch data from the server
    async function fetchData() {
        try {
            // Reset monthly fine and reward values if it's a new month
            resetMonthlyValues();

            const response = await fetch('/get_data');
            const data = await response.json();

            console.log("Received data:", data);  // Log for debugging

            // Update the live flow rate display
            document.getElementById('flow-rate').textContent = `${data.flow_rate} L/min`;

            // Update the timestamp
            document.getElementById('timestamp').textContent = data.timestamp;

            // Add a new row to the recent readings table
            const table = document.getElementById('data-table');
            const newRow = table.insertRow(1); // Insert at the top, below headers
            const timestampCell = newRow.insertCell(0);
            const flowRateCell = newRow.insertCell(1);

            // Populate cells with data
            timestampCell.textContent = data.timestamp;
            flowRateCell.textContent = `${data.flow_rate} L/min`;

            // Check for high or low water usage and update fine and reward
            if (data.flow_rate > highUsageThreshold) {
                alert(`High Water Usage Alert - Your usage is too high! Current flow rate is ${data.flow_rate} L/min`);
                fine = (data.flow_rate - highUsageThreshold) * 10; // Example fine calculation
            } else if (data.flow_rate < lowUsageThreshold) {
                alert(`Low Water Usage Alert - Your usage is too low! Keep it up! Current flow rate is ${data.flow_rate} L/min`);
                reward = (lowUsageThreshold - data.flow_rate) * 5; // Example reward calculation
            }

            // Update the fine and reward values in the display
            document.getElementById('fine').textContent = fine.toFixed(2); // Display fine
            document.getElementById('reward').textContent = reward.toFixed(2); // Display reward

        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    // Poll for data every 5 seconds
    setInterval(fetchData, 5000);
    fetchData(); // Fetch data immediately on page load
});
