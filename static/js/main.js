document.addEventListener('DOMContentLoaded', () => {
    // Define water usage thresholds
    const highUsageThreshold = 80.0;  // High usage threshold
    const lowUsageThreshold = 10.0;   // Low usage threshold

    // Initialize the virtual wallet to store the total fine and reward
    let totalFine = 0;
    let totalReward = 0;

    // Get the current month and year at page load
    let currentMonth = new Date().getMonth();  // 0-based month index
    let currentYear = new Date().getFullYear(); // Current year
    let firstDayOfCurrentMonth = new Date(currentYear, currentMonth, 1); // First day of current month

    // Function to reset fine and reward at the start of a new month
    function resetMonthlyValues() {
        const today = new Date();
        
        // Check if today is the first day of the new month
        if (today.getDate() === 1) {
            totalFine = 0;
            totalReward = 0;
            // Update the current month and year
            currentMonth = today.getMonth();
            currentYear = today.getFullYear();
            firstDayOfCurrentMonth = new Date(currentYear, currentMonth, 1);
            console.log("New month started! Wallet values reset.");
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
                const fineAmount = (data.flow_rate - highUsageThreshold) * 10;  // Example fine calculation
                totalFine += fineAmount;  // Add the fine to the wallet
            } else if (data.flow_rate < lowUsageThreshold) {
                alert(`Low Water Usage Alert - Your usage is too low! Keep it up! Current flow rate is ${data.flow_rate} L/min`);
                const rewardAmount = (lowUsageThreshold - data.flow_rate) * 5;  // Example reward calculation
                totalReward += rewardAmount;  // Add the reward to the wallet
            }

            // Update the fine and reward values in the display
            document.getElementById('fine').textContent = totalFine.toFixed(2);  // Display total fine
            document.getElementById('reward').textContent = totalReward.toFixed(2);  // Display total reward

            // Display the total wallet balance
            document.getElementById('wallet').textContent = `Wallet Balance: Rs ${totalFine.toFixed(2)} Fine, ${totalReward.toFixed(2)} L Reward`;

        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    // Poll for data every 5 seconds
    setInterval(fetchData, 5000);
    fetchData(); // Fetch data immediately on page load
});
