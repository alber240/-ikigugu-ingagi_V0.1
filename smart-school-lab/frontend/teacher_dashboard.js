// ✅ Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * 🔹 Ensure `#deviceList` exists before running functions
 */
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔍 Checking if #deviceList exists...");

  let container = document.getElementById("deviceList");

  if (!container) {
    console.error("❌ '#deviceList' not found! Creating dynamically.");
    container = document.createElement("div");
    container.id = "deviceList";

    const deviceSection = document.querySelector(".device-controls");
    if (deviceSection) {
      deviceSection.appendChild(container);
      console.warn("✅ '#deviceList' created inside .device-controls.");
    } else {
      document.body.appendChild(container);
      console.warn("⚠️ '#deviceList' created in <body>, check HTML structure.");
    }
  }

  console.log("✅ #deviceList verified!");
  loadActivityLogs();
  loadDeviceAnalytics();
  loadTeacherDevices();
});

/**
 * 🔹 Fetch and display activity logs dynamically
 */
async function loadActivityLogs() {
  try {
    const res = await fetch(`${API_BASE_URL}/logs`);
    if (!res.ok) throw new Error(`Failed to fetch logs: ${res.statusText}`);

    const logs = await res.json();
    const logTable = document.getElementById("logTableBody");

    if (!logTable) {
      console.error("Error: Element 'logTableBody' not found! Check HTML structure.");
      return;
    }

    logTable.innerHTML = ""; // ✅ Clear previous entries

    logs.forEach(log => {
      const row = `<tr>
        <td>${log.username || "Unknown"}</td>
        <td>${log.device || "Unknown Device"}</td>
        <td>${log.action?.toUpperCase() || "Unknown Action"}</td>
        <td>${log.timestamp || "No Time Available"}</td>
      </tr>`;
      logTable.innerHTML += row;
    });

    console.log("Activity logs loaded successfully!");
  } catch (error) {
    console.error("Error loading activity logs:", error);
  }
}

/**
 * 🔹 Toggle Device ON/OFF
 */
window.toggleDevice = async function(deviceId) { 
  try {
    console.log(`🔍 Attempting to toggle Device ID: ${deviceId}`);

    const deviceElem = document.querySelector(`.device[data-id="${deviceId}"] input[type="checkbox"]`);
    
    if (!deviceElem) {
      console.error(`❌ Error: Checkbox for Device ID ${deviceId} not found!`);
      return;
    }

    console.log(`✅ Checkbox found for Device ID ${deviceId}, current state: ${deviceElem.checked}`);

    const isOn = deviceElem.checked;

    const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: isOn ? "on" : "off" })
    });

    if (!res.ok) throw new Error(`Error toggling Device ${deviceId}`);

    alert(`Device ${deviceId} is now ${isOn ? "ON" : "OFF"}`);
    loadTeacherDevices(); // ✅ Refresh UI after toggling
  } catch (error) {
    console.error(`❌ Error toggling Device ${deviceId}:`, error);
  }
};

/**
 * 🔹 Fetch and display device analytics
 */
async function loadDeviceAnalytics() {
  try {
    const res = await fetch(`${API_BASE_URL}/devices/analytics`);
    if (!res.ok) throw new Error(`Error fetching analytics: ${res.statusText}`);

    const data = await res.json();
    const analyticsContainer = document.getElementById("analyticsSection");

    if (!analyticsContainer) {
      console.error("Error: Element 'analyticsSection' not found! Check HTML structure.");
      return;
    }

    analyticsContainer.innerHTML = ""; // ✅ Clear previous data

    data.forEach(device => {
      const analyticsCard = `
        <div class="device-analytics">
          <h3>${device.name}</h3>
          <p>Status: ${device.status}</p>
          <p>Total Usage: ${device.total_usage_hours ? device.total_usage_hours.toFixed(2) : "N/A"} hrs</p>
        </div>
      `;
      analyticsContainer.innerHTML += analyticsCard;
    });

    console.log("Device analytics loaded successfully!");
  } catch (error) {
    console.error("Failed to load device analytics:", error);
  }
}

/**
 * 🔹 Fetch and display all devices for teachers dynamically
 */
async function loadTeacherDevices() {
  try {
    const container = document.getElementById("deviceList");

    if (!container) {
      console.error("Error: Element '#deviceList' not found! Creating dynamically.");
      
      container = document.createElement("div");
      container.id = "deviceList";

      const deviceSection = document.querySelector(".device-controls");
      if (deviceSection) {
        deviceSection.appendChild(container);
        console.warn("✅ '#deviceList' created inside .device-controls.");
      } else {
        document.body.appendChild(container);
        console.warn("⚠️ '#deviceList' created in <body>, check HTML structure.");
      }
    }

    const res = await fetch(`${API_BASE_URL}/devices`);
    if (!res.ok) throw new Error(`Error fetching devices: ${res.statusText}`);

    const devices = await res.json();
    container.innerHTML = ""; // ✅ Clear previous entries

    devices.forEach(device => {
      const deviceDiv = document.createElement("div");
      deviceDiv.className = "device";
      deviceDiv.dataset.id = device.id;

      const span = document.createElement("span");
      span.textContent = device.name;

      const checkbox = document.createElement("input"); 
      checkbox.type = "checkbox"; // ✅ Ensure checkboxes exist
      checkbox.checked = device.status === "on";
      checkbox.addEventListener("change", () => toggleDevice(device.id)); 

      deviceDiv.appendChild(span);
      deviceDiv.appendChild(checkbox); 
      container.appendChild(deviceDiv);

      console.log(`✅ Device added: ${device.name}, ID: ${device.id}`);
    });

    console.log("Devices loaded successfully!");
  } catch (error) {
    console.error("Failed to load devices:", error);
  }
}
