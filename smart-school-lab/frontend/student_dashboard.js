// Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * Fetch all devices from the backend and display only accessible ones for students
 */
async function loadStudentDevices() {
  try {
    // Send GET request to the API to retrieve devices
    const res = await fetch(`${API_BASE_URL}/devices`);
    const devices = await res.json();

    // Select the container for displaying devices
    const container = document.querySelector(".device-status");
    container.innerHTML = "<h3>Accessible Devices</h3>";

    // Iterate through the devices and render them dynamically
    devices.forEach(device => {
      const deviceDiv = document.createElement("div");
      deviceDiv.className = "device";

      deviceDiv.innerHTML = `
        <span>${device.name}</span>
        <span class="status ${device.status}">${device.status.toUpperCase()}</span>
      `;

      // Append each device to the container
      container.appendChild(deviceDiv);
    });

    console.log("Student view loaded successfully!");

  } catch (error) {
    console.error("Failed to fetch student view:", error);
  }
}

/**
 * Initialize the student dashboard when the page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.includes("student_dashboard.html")) {
    loadStudentDevices();
  }
});
