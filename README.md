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

# 📚 Smart School Lab Project

## 🔹 Overview
Smart School Lab is an innovative platform designed to enable teachers to **manage and control devices in a classroom environment**, track student activities, and provide analytics for better decision-making.

## 📆 Project Roadmap
### ✅ Completed Tasks (Week 1)
- **System Architecture Defined** ✅
- **Database Schema Designed** ✅
- **API Routes Structured** ✅
- **Frontend & Backend Skeleton Set Up** ✅
- **Initial GitHub Setup & Workflow Defined** ✅

### 🚀 Ongoing Work (Week 2)
- **Frontend-Backend Integration** 🏗
- **Authentication System Development** 🏗
- **Device Control Features (Toggle On/Off)** 🏗
- **UI Refinements and Testing** 🏗

### 🛠 Upcoming Work (Week 3 - Week 4)
- **Automated Device Control Features**
- **Device Status Monitoring and Reporting**
- **Comprehensive Testing and Bug Fixes**
- **Deployment and Documentation Finalization**

## 🔹 Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python), REST APIs  
- **Database:** JSON / SQLite  
- **Version Control:** GitHub  

## 🔹 Setup Instructions
### 🛠 How to Run Locally
1️⃣ Clone the repository:  
   ```bash
   git clone https://github.com/alber240/-ikigugu-ingagi_V0.1.git
   cd smart-school-lab


# Flask JWT Authentication System 🚀

## ✅ Progress Summary
- Implemented **JWT-based authentication** (login, protected routes, token refresh).
- Added **automatic token refresh** to prevent expiration issues.
- Integrated **role-based access control** (Admin, Teacher, Student).
- Developed **secure API endpoints** for managing authentication.
- Tested functionality using **Postman & JavaScript automation**.

## ✅ How to Use
1️⃣ **Clone the repository**:
