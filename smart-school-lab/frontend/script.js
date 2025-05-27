// ---------------------------------------------
// 🔹 AUTHENTICATION: LOGIN & TOKEN MANAGEMENT
// ---------------------------------------------

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();  // ✅ Prevent default form submission

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        const response = await fetch("http://localhost:5000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✅ Login successful!`);

            // ✅ Store tokens securely in sessionStorage
            sessionStorage.setItem("access_token", data.access_token);
            sessionStorage.setItem("refresh_token", data.refresh_token);
            sessionStorage.setItem("username", username);  // ✅ Store username for session tracking

            window.location.href = "dashboard.html";  // ✅ Redirect user after successful login
        } else {
            alert(`❌ Login failed: ${data.error}`);
        }
    } catch (error) {
        console.error("Login failed:", error);
        alert("❌ Error logging in. Try again later.");
    }
});

// ---------------------------------------------
// 🔹 AUTO-REFRESH TOKENS BEFORE EXPIRATION
// ---------------------------------------------

async function fetchWithAutoRefresh(url, options = {}) {
    let accessToken = sessionStorage.getItem("access_token");

    options.headers = options.headers || {};  // ✅ Ensure headers exist
    options.headers["Authorization"] = `Bearer ${accessToken}`;

    let response = await fetch(url, options);

    if (response.status === 401) {  // 🔥 If access token expired, attempt refresh
        const refreshToken = sessionStorage.getItem("refresh_token");

        const refreshResponse = await fetch("http://localhost:5000/auth/refresh", {
            method: "POST",
            headers: { "Authorization": `Bearer ${refreshToken}` }
        });

        if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json();
            sessionStorage.setItem("access_token", refreshData.access_token);
            sessionStorage.setItem("refresh_token", refreshData.refresh_token);

            // 🔄 Retry original request with new access token
            options.headers["Authorization"] = `Bearer ${refreshData.access_token}`;
            return fetch(url, options);
        } else {
            alert("❌ Session expired, please log in again.");
            window.location.href = "login.html";  // ✅ Redirect user to login page
        }
    }

    return response;
}

// ---------------------------------------------
// 🔹 FETCH PROTECTED DATA USING AUTO-REFRESH
// ---------------------------------------------

async function fetchProtectedData() {
    try {
        const response = await fetchWithAutoRefresh("http://localhost:5000/auth/protected-route", { method: "GET" });
        const data = await response.json();

        if (response.ok) {
            console.log("✅ Protected Data:", data);
            document.getElementById("protectedContent").textContent = data.message;
        } else {
            console.error("❌ Error accessing protected data:", data.error);
        }
    } catch (error) {
        console.error("❌ Network error:", error);
    }
}

// ---------------------------------------------
// 🔹 ROLE-BASED ACCESS CONTROL (Admin vs User)
// ---------------------------------------------

async function loadDashboard() {
    const username = sessionStorage.getItem("username") || "Unknown";

    try {
        const response = await fetchWithAutoRefresh("http://localhost:5000/users/role", { method: "GET" });
        const data = await response.json();

        if (response.ok) {
            const userRole = data.role.toLowerCase();
            console.log("DEBUG: User role →", userRole);

            if (userRole === "teacher") {
                window.location.href = "teacher_dashboard.html";
            } else if (userRole === "student") {
                window.location.href = "student_dashboard.html";
            } else {
                alert("❌ Role not recognized!");
            }
        } else {
            console.error("❌ Error retrieving user role:", data.error);
        }
    } catch (error) {
        console.error("❌ Network error:", error);
    }
}

// ---------------------------------------------
// 🔹 DEVICE CONTROL USING AUTO-REFRESH TOKENS
// ---------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtns = document.querySelectorAll(".toggle-btn");

    if (toggleBtns.length > 0) {
        toggleBtns.forEach((btn) => {
            btn.addEventListener("click", async () => {
                const deviceId = btn.dataset.deviceId;
                try {
                    const response = await fetchWithAutoRefresh(`http://localhost:5000/devices/${deviceId}/toggle`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" }
                    });

                    const data = await response.json();
                    if (!response.ok) throw new Error(data.error || "Failed to toggle device.");

                    alert(`✅ ${data.message}`);
                    btn.textContent = data.device.status === "on" ? "Turn Off" : "Turn On";
                } catch (error) {
                    alert("❌ Error toggling device.");
                    console.error(error);
                }
            });
        });
    }
});

// ---------------------------------------------
// 🔹 LOGS PAGE: FETCH USER HISTORY
// ---------------------------------------------

const logsTable = document.getElementById("logsTable");

if (logsTable) {
    fetchLogs();
}

async function fetchLogs() {
    try {
        const response = await fetchWithAutoRefresh("http://localhost:5000/logs", { method: "GET" });
        const logs = await response.json();

        logs.forEach(log => {
            const username = log.username.trim() === "Unknown" ? "System User" : log.username;
            const row = document.createElement("tr");
            row.innerHTML = `<td>${username}</td><td>${log.device}</td><td>${log.action}</td><td>${log.timestamp}</td>`;
            logsTable.appendChild(row);
        });
    } catch (error) {
        console.error("❌ Error loading logs:", error);
    }
}
