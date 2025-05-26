// ✅ Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * 🔹 Fetch all accessible devices for students dynamically
 */
async function loadStudentDevices() {
  try {
    const res = await fetch(`${API_BASE_URL}/devices`);
    if (!res.ok) throw new Error(`Error fetching student devices: ${res.statusText}`);

    const devices = await res.json();
    const container = document.querySelector(".device-status");

    if (!container) {
      console.error("Element '.device-status' not found! Check HTML structure.");
      return;
    }

    container.innerHTML = "<h3>Accessible Devices</h3>";

    devices.forEach(device => {
      const deviceDiv = document.createElement("div");
      deviceDiv.className = "device";

      deviceDiv.innerHTML = `
        <span>${device.name}</span>
        <span class="status ${device.status}">${device.status.toUpperCase()}</span>
        <button class="request-access" data-device-id="${device.id}">Request Access</button>
      `;

      container.appendChild(deviceDiv);
    });

    console.log("Student view loaded successfully!");
    attachRequestListeners(); // ✅ Attach event listeners correctly after elements exist

  } catch (error) {
    console.error("Failed to fetch student view:", error);
  }
}

/**
 * 🔹 Allow students to request access for devices
 */
function attachRequestListeners() {
  document.addEventListener("click", async (event) => {
    if (event.target.classList.contains("request-access")) {
      const deviceId = event.target.dataset.deviceId;
      const username = sessionStorage.getItem("username") || "Unknown"; // ✅ Capture username

      try {
        const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/request-access`, { 
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ device_id: deviceId, username }) 
        });

        if (!res.ok) throw new Error(`Failed to request access for Device ${deviceId}`);

        alert(`Access request for ${deviceId} sent successfully!`);
        loadStudentDevices(); // ✅ Refresh device list after request

      } catch (error) {
        console.error(`Error requesting access for Device ${deviceId}:`, error);
      }
    }
  });
}

/**
 * 🔹 Initialize student dashboard when the page loads
 */
document.addEventListener("DOMContentLoaded", loadStudentDevices);
