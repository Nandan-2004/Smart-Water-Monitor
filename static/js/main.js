document.addEventListener('DOMContentLoaded', () => {
    // Establish connection with the Socket.IO server
    const socket = io.connect('http://127.0.0.1:5000');

    socket.on('connect', () => {
        console.log('Successfully connected to the server');
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection failed:', error);
    });

    // Define the updateData function to emit new data or handle actions every minute
    function updateData() {
        console.log("Fetching new data from server...");
        socket.emit('request_data'); // Assuming the server listens for 'request_data' and sends 'new_data' in response
    }

    // Listen for the 'new_data' event from the server
    socket.on('new_data', function(data) {
        if (data && data.flow_rate && data.timestamp) {
            console.log("Received data:", data);  // Confirms event was received
            document.getElementById('flow-rate').textContent = `${data.flow_rate} L/min`;
            document.getElementById('timestamp').textContent = data.timestamp;

            const table = document.getElementById('data-table');
            const newRow = table.insertRow(1); // Insert at the top, below headers
            const timestampCell = newRow.insertCell(0);
            const flowRateCell = newRow.insertCell(1);

            timestampCell.textContent = data.timestamp;
            flowRateCell.textContent = `${data.flow_rate} L/min`;
        } else {
            console.error('Invalid data received:', data);
        }
    });

    // Set interval to update data every 60 seconds
    setInterval(updateData, 60000);

    // Initial data update
    updateData();
});
