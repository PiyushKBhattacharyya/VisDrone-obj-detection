// Wait until the DOM is fully loaded before executing
document.addEventListener("DOMContentLoaded", function () {

    // Get the elements for video and dataset display
    const videoElement = document.getElementById('video');
    const datasetElement = document.getElementById('dataset');

    // WebSocket connection for live video feed
    const socket = new WebSocket('ws://localhost:8000/video_feed');  // Change URL for cloud server if needed

    // Update the video source when a new frame is received
    socket.onmessage = function(event) {
        // Set the live video feed as the new image source
        videoElement.src = event.data;
    };

    // Function to fetch the real-time dataset images
    async function fetchDataset() {
        try {
            const response = await fetch('/dataset');  // Fetch the dataset from the backend
            const data = await response.json();  // Parse the JSON response

            // Clear the existing images in the dataset section
            datasetElement.innerHTML = '';

            // Loop through the images and append them to the dataset section
            data.images.forEach(image => {
                const imgElement = document.createElement('img');
                imgElement.src = `Dataset/${image}`;  // Assuming the images are saved under 'Dataset' folder
                imgElement.alt = 'Detected Person';  // Optional: Add alt text for accessibility
                datasetElement.appendChild(imgElement);  // Append each image to the dataset container
            });
        } catch (error) {
            console.error("Error fetching dataset:", error);
        }
    }

    // Update the dataset images every 3 seconds
    setInterval(fetchDataset, 3000);  // Adjust the interval time as needed (in milliseconds)
});
