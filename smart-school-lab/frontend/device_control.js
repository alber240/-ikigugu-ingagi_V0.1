// Define API Base URL
const API_BASE_URL = "http://localhost:5000";
let deviceId = 2; // Hardcoded for now, can be made dynamic later

/**
 * Fetch and display device details from the backend
 */
async function loadDeviceDetail() {
  try {
    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}`);
    
    if (!res.ok) {
      throw new Error(`Error fetching device: ${res.statusText}`);
    }

    const device = await res.json();

    // Update UI with device info
    document.getElementById("deviceName").textContent = device.name;
    document.getElementById("deviceStatus").textContent = device.status.toUpperCase();
    document.getElementById("togglePowerBtn").textContent = device.status === "on" ? "Turn Off" : "Turn On";

  } catch (error) {
    console.error("Failed to load device details:", error);
  }
}

/**
 * Toggle device ON/OFF
 */
async function toggleDevice() {
  try {
    const currentStatus = document.getElementById("deviceStatus").textContent.toLowerCase();
    const newStatus = currentStatus === "on" ? "off" : "on";

    // ✅ Corrected API endpoint for toggling
    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/toggle`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: newStatus }) // ✅ Correct request format
    });

    if (!res.ok) {
      throw new Error(`Error toggling device: ${res.statusText}`);
    }

    loadDeviceDetail(); // Refresh device details after toggling

  } catch (error) {
    console.error("Error toggling device:", error);
  }
}

/**
 * Save schedule settings
 */
async function saveSchedule() {
  try {
    const onTime = document.getElementById("startTime").value;
    const offTime = document.getElementById("endTime").value;

    // ✅ Ensure values exist before sending request
    if (!onTime || !offTime) {
      alert("Please enter both start and end times before setting a schedule.");
      return;
    }

    const confirmToday = confirm("Do you want to apply this schedule for today?");
    if (!confirmToday) return; // ✅ Prevent request if user cancels

    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/schedule`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ on_time: onTime, off_time: offTime }) // ✅ Correct data format
    });

    if (!res.ok) {
      throw new Error(`Error saving schedule: ${res.statusText}`);
    }

    alert("Schedule saved successfully!");

  } catch (error) {
    console.error("Failed to save schedule:", error);
  }
}


/**
 * Load and display device usage history
 */
async function loadUsageHistory() {
  try {
    // ✅ Corrected API endpoint for fetching logs
    const res = await fetch(`${API_BASE_URL}/logs`); 
    
    if (!res.ok) {
      throw new Error(`Error fetching logs: ${res.statusText}`);
    }

    const logs = await res.json();

    // Select the table body for usage history
    const tbody = document.getElementById("usageLogTable");
    tbody.innerHTML = ""; // Clear previous entries

    // Populate log entries dynamically
    logs.forEach(log => {
      const row = `<tr>
        <td>${log.user}</td>
        <td>${log.action.toUpperCase()}</td>
        <td>${log.time}</td>
      </tr>`;
      tbody.innerHTML += row;
    });

    console.log("Usage history loaded successfully!");

  } catch (error) {
    console.error("Failed to load usage history:", error);
  }
}

/**
 * Initialize script when the page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  // Load device details and usage history on page load
  loadDeviceDetail();
  loadUsageHistory();

  // Attach event listeners only if elements exist
  const toggleBtn = document.getElementById("togglePowerBtn");
  const scheduleBtn = document.getElementById("setScheduleBtn");

  if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleDevice);
  } else {
    console.error("Element 'togglePowerBtn' not found!");
  }

  if (scheduleBtn) {
    scheduleBtn.addEventListener("click", saveSchedule);
  } else {
    console.error("Element 'setScheduleBtn' not found!");
  }
});
