// ✅ Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * 🔹 Fetch & display ALL devices dynamically from the backend
 */
async function loadTeacherDevices() {
  try {
    const res = await fetch(`${API_BASE_URL}/devices`); // ✅ Fixed trailing slash issue
    if (!res.ok) throw new Error(`Error fetching devices: ${res.statusText}`);

    const devices = await res.json();
    const container = document.getElementById("deviceList");

    if (!container) {
      console.error("Error: Element '#deviceList' not found! Check HTML structure.");
      return;
    }

    container.innerHTML = ""; // ✅ Clear previous entries

    devices.forEach(device => {
      const deviceDiv = document.createElement("div");
      deviceDiv.className = "device";
      deviceDiv.dataset.id = device.id;

      deviceDiv.innerHTML = `
        <span>${device.name}</span>
        <button onclick="toggleDevice(${device.id})">${device.status === "on" ? "Turn Off" : "Turn On"}</button>
      `;

      container.appendChild(deviceDiv);
    });

    console.log("Devices loaded successfully!");
  } catch (error) {
    console.error("Failed to load devices:", error);
  }
}

/**
 * 🔹 Toggle ANY device ON/OFF
 */
async function toggleDevice(deviceId) {
  try {
    // ✅ Ensure the device status element exists before accessing
    const deviceStatusElem = document.getElementById("deviceStatus");
    if (!deviceStatusElem) {
      console.error("Error: Element 'deviceStatus' not found!");
      return;
    }

    // ✅ Determine current status dynamically
    const currentStatus = deviceStatusElem.textContent.toLowerCase();
    const newStatus = currentStatus === "on" ? "off" : "on"; 

    const username = sessionStorage.getItem("username") || "Unknown";

    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/toggle`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: newStatus, username }) // ✅ Send correct new status
    });

    if (!res.ok) throw new Error(`Error toggling Device ${deviceId}`);

    alert(`Device ${deviceId} is now ${newStatus.toUpperCase()}`);

    loadTeacherDevices(); // ✅ Refresh devices
    loadUsageHistory();  // ✅ Refresh history
  } catch (error) {
    console.error(`Error toggling Device ${deviceId}:`, error);
  }
}

/**
 * 🔹 Save schedule settings
 */
async function saveSchedule(deviceId) {
  try {
    const onTime = document.getElementById("startTime")?.value;
    const offTime = document.getElementById("endTime")?.value;
    const username = sessionStorage.getItem("username") || "Unknown"; // ✅ Capture username

    if (!onTime || !offTime) {
      alert("Error: Please enter both Start and End times.");
      return;
    }

    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/schedule`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ on_time: onTime, off_time: offTime, username })
    });

    if (!res.ok) throw new Error(`Error saving schedule for Device ${deviceId}`);

    alert(`Schedule set for ${deviceId} successfully!`);
    
    loadUsageHistory(); // ✅ Update history after scheduling
  } catch (error) {
    console.error(`Failed to save schedule for Device ${deviceId}:`, error);
  }
}

/**
 * 🔹 Load & display device usage history dynamically
 */
async function loadUsageHistory() {
  try {
    const tbody = document.getElementById("usageLogTable");

    // ✅ Ensure usage log table exists before execution
    if (!tbody) {
      console.error("Error: Element 'usageLogTable' not found! Check HTML structure.");
      return;
    }

    const res = await fetch(`${API_BASE_URL}/logs`);
    if (!res.ok) throw new Error(`Error fetching logs: ${res.statusText}`);

    const logs = await res.json();
    tbody.innerHTML = ""; // ✅ Clear previous entries

    logs.forEach(log => {
      const username = log.username || "Unknown";
      const device = log.device || "Unknown Device";
      const timestamp = log.timestamp || "No Time Available";

      const row = `<tr>
        <td>${username}</td>
        <td>${device}</td>
        <td>${log.action?.toUpperCase() || "Unknown Action"}</td>
        <td>${timestamp}</td>
      </tr>`;
      tbody.innerHTML += row;
    });

    console.log("Usage history loaded successfully!");
  } catch (error) {
    console.error("Failed to load usage history:", error);
  }
}

/**
 * 🔹 Initialize script when the page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  loadTeacherDevices();
  loadUsageHistory();
});
