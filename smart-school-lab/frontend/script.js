const statusEl = document.getElementById("status");
const bulbEl = document.getElementById("bulb");

function fetchStatus() {
  fetch("http://127.0.0.1:5000/device/status")
    .then((res) => res.json())
    .then((data) => {
      statusEl.textContent = data.status.toUpperCase();
      bulbEl.src =
        data.status === "on"
          ? "https://img.icons8.com/ios-filled/100/light-on.png"
          : "https://img.icons8.com/ios/100/light-off.png";
    });
}

function toggleDevice(action) {
  fetch("http://127.0.0.1:5000/device/toggle", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ action }),
  })
    .then((res) => res.json())
    .then(() => fetchStatus());
}

fetchStatus();
