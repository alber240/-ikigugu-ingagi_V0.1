// ✅ Define API Base URL
const API_BASE_URL = "http://localhost:5000";

/**
 * 🔹 Fetch and display logs dynamically
 */
async function loadLogs() {
  try {
    // ✅ Get the selected device filter value (with fallback)
    const filterDevice = document.getElementById("filterDevice")?.value || "All";

    // ✅ Construct API URL with query parameters
    let url = `${API_BASE_URL}/logs`;
    if (filterDevice !== "All") {
      url += `?device=${encodeURIComponent(filterDevice)}`; // ✅ Prevent query string issues
    }

    // ✅ Fetch logs from backend API
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`Error fetching logs: ${res.statusText}`);
    }

    const logs = await res.json();

    // ✅ Select the table body where logs will be displayed
    const tbody = document.querySelector(".logs-table tbody");
    if (!tbody) {
      console.error("Element '.logs-table tbody' not found!");
      return;
    }

    tbody.innerHTML = ""; // ✅ Clear previous entries

    // ✅ Populate table rows dynamically
    logs.forEach(log => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${log.timestamp || "No Time Available"}</td>  <!-- ✅ Fixed missing time field -->
        <td>${log.device || "Unknown Device"}</td>
        <td>${log.username || "Unknown User"}</td>
        <td>${log.action.toUpperCase() || "Unknown Action"}</td>
      `;
      tbody.appendChild(row);
    });

    console.log("Logs successfully loaded!");

  } catch (error) {
    console.error("Failed to load logs:", error);
  }
}

/**
 * 🔹 Event listener for device filter change
 */
document.addEventListener("DOMContentLoaded", () => {
  const filterDevice = document.getElementById("filterDevice");

  if (filterDevice) {
    filterDevice.addEventListener("change", loadLogs);
  } else {
    console.error("Element 'filterDevice' not found!");
  }

  // ✅ Load logs when the logs page is loaded
  if (window.location.pathname.includes("logs.html")) {
    loadLogs();
  }
});
