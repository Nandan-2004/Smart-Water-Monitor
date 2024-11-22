// /api/data.js

export default async function handler(req, res) {
    if (req.method === 'POST') {
      try {
        // Parse the incoming JSON data
        const { flowRate, totalLiters } = req.body;
  
        // Example of logging the received data
        console.log(`Received Flow Rate: ${flowRate} L/min`);
        console.log(`Received Total Liters: ${totalLiters} L`);
  
        // Here you can process the data, save it to a database, or any other logic
  
        // Respond with a success message
        res.status(200).json({ message: 'Data received successfully!' });
      } catch (error) {
        // Handle errors
        console.error('Error handling POST request:', error);
        res.status(500).json({ error: 'Internal server error' });
      }
    } else {
      // If the request method is not POST, return a method not allowed response
      res.status(405).json({ error: 'Method Not Allowed' });
    }
  }
  