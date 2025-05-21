// Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * Load all devices from the backend and render them dynamically
 */
async function loadTeacherDevices() {
  try {
    // Fetch all devices from the API
    const res = await fetch(`${API_BASE_URL}/devices`);
    const devices = await res.json();

    // Select the container where devices will be displayed
    const container = document.querySelector(".device-controls");
    container.innerHTML = ""; // Clear previous entries

    // Iterate through the devices and dynamically create HTML elements
    devices.forEach(device => {
      const deviceDiv = document.createElement("div");
      deviceDiv.className = "device";
      deviceDiv.dataset.id = device.id;

      deviceDiv.innerHTML = `
        <span>${device.name}</span>
        <label class="switch">
          <input type="checkbox" ${device.status === "on" ? "checked" : ""}>
          <span class="slider round"></span>
        </label>
      `;

      // Add an event listener for toggling the device status
      deviceDiv.querySelector("input").addEventListener("change", (event) => {
        toggleDevice(device.id, event.target.checked);
      });

      // Append the device element to the container
      container.appendChild(deviceDiv);
    });

  } catch (error) {
    console.error("Failed to load devices:", error);
  }
}

/**
 * Toggle the status of a device (ON/OFF)
 * @param {number} deviceId - ID of the device
 * @param {boolean} isOn - True if ON, False if OFF
 */
async function toggleDevice(deviceId, isOn) {
  try {
    // Send the toggle request to the API
    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: isOn ? "on" : "off" })
    });

    // Check if the response is OK, otherwise show an alert
    if (!res.ok) {
      alert("Error updating device.");
    }

    // Reload devices after toggle to reflect changes
    loadTeacherDevices();

  } catch (error) {
    console.error("Error toggling device:", error);
  }
}

/**
 * Initialize dashboard functionality when the page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.includes("teacher_dashboard.html")) {
    loadTeacherDevices();
  }
});
