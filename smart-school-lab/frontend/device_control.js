// ---------------------------------------------
// 🔹 API Base URL (Modify if backend URL changes)
// ---------------------------------------------
const API_BASE_URL = "http://localhost:5000";

/**
 * 🔹 Fetch & display ALL devices dynamically from the backend
 */
async function loadTeacherDevices() {
  try {
    const container = document.getElementById("deviceList");

    // ✅ Ensure deviceList exists before proceeding
    if (!container) {
      console.error("❌ Error: Element '#deviceList' not found! Check HTML structure.");
      return;
    }

    console.log("✅ Found #deviceList element, loading devices...");

    // ✅ Fetch devices from backend
    const res = await fetch(`${API_BASE_URL}/devices`);
    if (!res.ok) throw new Error(`Error fetching devices: ${res.statusText}`);

    const devices = await res.json();
    container.innerHTML = ""; // ✅ Clear previous entries

    // ✅ Populate device list dynamically
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

    console.log("✅ Devices loaded successfully!");
  } catch (error) {
    console.error("❌ Failed to load devices:", error);
  }
}

/**
 * 🔹 Toggle ANY device ON/OFF
 */
async function toggleDevice(deviceId) {
  try {
    const deviceStatusElem = document.getElementById("deviceStatus");

    // ✅ Ensure status element exists before accessing it
    if (!deviceStatusElem) {
      console.error("❌ Error: Element '#deviceStatus' not found!");
      return;
    }

    const currentStatus = deviceStatusElem.textContent.toLowerCase();
    const newStatus = currentStatus === "on" ? "off" : "on"; 
    const username = sessionStorage.getItem("username") || "Unknown";

    // ✅ Send toggle request to backend
    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/toggle`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: newStatus, username })
    });

    if (!res.ok) throw new Error(`Error toggling Device ${deviceId}`);

    alert(`✅ Device ${deviceId} is now ${newStatus.toUpperCase()}`);

    loadTeacherDevices(); // ✅ Refresh devices
    loadUsageHistory();  // ✅ Refresh usage history
  } catch (error) {
    console.error(`❌ Error toggling Device ${deviceId}:`, error);
  }
}

/**
 * 🔹 Save schedule settings
 */
async function saveSchedule(deviceId) {
  try {
    const onTime = document.getElementById("startTime")?.value;
    const offTime = document.getElementById("endTime")?.value;
    const username = sessionStorage.getItem("username") || "Unknown";

    if (!onTime || !offTime) {
      alert("❌ Error: Please enter both Start and End times.");
      return;
    }

    // ✅ Send schedule request to backend
    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/schedule`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ on_time: onTime, off_time: offTime, username })
    });

    if (!res.ok) throw new Error(`Error saving schedule for Device ${deviceId}`);

    alert(`✅ Schedule set for ${deviceId} successfully!`);
    
    loadUsageHistory(); // ✅ Update history after scheduling
  } catch (error) {
    console.error(`❌ Failed to save schedule for Device ${deviceId}:`, error);
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
      console.error("❌ Error: Element '#usageLogTable' not found! Check HTML structure.");
      return;
    }

    // ✅ Fetch logs from backend
    const res = await fetch(`${API_BASE_URL}/logs`);
    if (!res.ok) throw new Error(`Error fetching logs: ${res.statusText}`);

    const logs = await res.json();
    tbody.innerHTML = ""; // ✅ Clear previous entries

    // ✅ Populate log history dynamically
    logs.forEach(log => {
      const row = `<tr>
        <td>${log.username || "System User"}</td>
        <td>${log.device || "Unknown Device"}</td>
        <td>${log.action?.toUpperCase() || "Unknown Action"}</td>
        <td>${log.timestamp || "No Time Available"}</td>
      </tr>`;
      tbody.innerHTML += row;
    });

    console.log("✅ Usage history loaded successfully!");
  } catch (error) {
    console.error("❌ Failed to load usage history:", error);
  }
}

async function deleteLogs() {
  // ✅ Show confirmation popup
  const confirmDelete = confirm("⚠️ Are you sure you want to delete logs older than 1 day? This action cannot be undone!");

  // ✅ If user cancels, stop the function
  if (!confirmDelete) {
    console.log("❌ Log deletion canceled by user.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/devices/delete-logs`, { method: "POST" });
    const data = await response.json();
    
    alert(data.message); // ✅ Show confirmation message
    loadUsageHistory();  // ✅ Refresh logs after cleanup
  } catch (error) {
    console.error("❌ Failed to delete logs:", error);
  }
}


/**
 * 🔹 Initialize script when the page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  loadTeacherDevices();
  loadUsageHistory();
});
