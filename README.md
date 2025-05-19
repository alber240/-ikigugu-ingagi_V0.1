# -ikigugu-ingagi_V0.1
Smart School Lab Manager - IoT Device Control Dashboard A web-based dashboard for managing and monitoring devices in school labs, aimed at optimizing power usage, ensuring security, and improving device management. 

## 🎨 UI Design

- Figma UI screens and wireframe documentation can be found in the `/UI Design/` folder.
- [Live Figma File](https://www.figma.com/design/QLUvX6RfQUvpt3G3HlDRmH/Smart-School--Community-?node-id=940-2&t=T3rOgphSV2zgBknz-0)

## for my ERD diagram for the Databas

# 💡 Smart School Lab Manager – IoT Lab

A web-based IoT solution for centralized control and monitoring of lab devices, developed under IKIGUGU GROUP LTD Industrial Attachment 2024–2025.

---

## 📡 API Documentation

These are the backend API routes for controlling devices, managing users, and logging activities. The backend is powered by **Flask**, and responses are in **JSON**.

### 🟢 Device Routes

| Method | Endpoint            | Description                  | Request Body                     | Response Example                          |
|--------|---------------------|------------------------------|----------------------------------|-------------------------------------------|
| `GET`  | `/device/status`    | Get current device status    | —                                | `{ "status": "on" }`                       |
| `POST` | `/device/toggle`    | Toggle device ON/OFF         | `{ "action": "on" \| "off" }`    | `{ "message": "Device turned on" }`       |

---

### 👤 User Routes (Mocked)

| Method | Endpoint         | Description                     | Request Body                                  | Response Example                                 |
|--------|------------------|---------------------------------|-----------------------------------------------|--------------------------------------------------|
| `GET`  | `/users`         | Get list of users               | —                                             | `[{"id": 1, "name": "Alice", "role": "teacher"}]` |
| `POST` | `/users`         | Add a new user                  | `{ "name": "John", "role": "student" }`       | `{ "message": "User added" }`                    |

---

### 📄 Logs Routes (Mocked)

| Method | Endpoint   | Description             | Request Body | Response Example                                   |
|--------|------------|-------------------------|--------------|----------------------------------------------------|
| `GET`  | `/logs`    | Get activity logs       | —            | `[{"id": 1, "action": "Turned ON", "by": "Admin"}]`|

---

### 🚦 Response Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid or missing data
- `404 Not Found`: Resource doesn’t exist

---

### 🔧 Notes

- All routes return data in JSON format.
- CORS is enabled for frontend access.
- Data is mocked for development purposes.

---

### ✅ Tested With

- [Postman](https://www.postman.com/) for API testing
- `fetch()` / `axios()` for frontend integration
