document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const role = document.getElementById('role').value;

  if (username && password && role) {
    // For now, we just simulate redirection
    if (role === 'teacher') {
      window.location.href = 'teacher_dashboard.html';
    } else {
      window.location.href = 'student_dashboard.html';
    }
  } else {
    alert('Please fill in all fields.');
  }
});

//Add Logic for Device Control and Logs

// --- DEVICE CONTROL LOGIC ---
document.addEventListener("DOMContentLoaded", () => {
  const deviceStatus = document.getElementById("deviceStatus");
  const toggleBtn = document.getElementById("togglePowerBtn");
  const usageLogTable = document.getElementById("usageLogTable");
  const setScheduleBtn = document.getElementById("setScheduleBtn");

  // Device Control Page Logic
  if (toggleBtn) {
    let isOn = false;

    toggleBtn.addEventListener("click", () => {
      isOn = !isOn;
      deviceStatus.textContent = isOn ? "ON" : "OFF";
      toggleBtn.textContent = isOn ? "Turn Off" : "Turn On";
      logUsage("Admin", isOn ? "Turned ON" : "Turned OFF", new Date().toLocaleString());
    });

    function logUsage(user, action, time) {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${user}</td><td>${action}</td><td>${time}</td>`;
      usageLogTable.appendChild(row);
    }

    // Mock initial usage history
    logUsage("Student", "Viewed Status", "2025-05-18 08:40 AM");
    logUsage("Admin", "Turned OFF", "2025-05-18 09:00 AM");
  }

  // Schedule button event (mock only)
  if (setScheduleBtn) {
    setScheduleBtn.addEventListener("click", () => {
      const startTime = document.getElementById("startTime").value;
      const endTime = document.getElementById("endTime").value;
      alert(`Schedule set from ${startTime} to ${endTime} (simulated)`);
    });
  }

  // --- LOGS PAGE LOGIC ---
  const logsTable = document.getElementById("logsTable");
  if (logsTable) {
    const mockLogs = [
      { user: "Admin", device: "Projector", action: "ON", time: "2025-05-19 09:00" },
      { user: "Student", device: "Computer 2", action: "Viewed", time: "2025-05-19 10:00" },
      { user: "Admin", device: "Lights", action: "OFF", time: "2025-05-19 11:00" },
      { user: "Student", device: "Computer 1", action: "Viewed", time: "2025-05-20 08:30" },
    ];

    mockLogs.forEach(log => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${log.user}</td>
        <td>${log.device}</td>
        <td>${log.action}</td>
        <td>${log.time}</td>
      `;
      logsTable.appendChild(row);
    });
  }
});

