### `models/device_model.py`

from .log_model import logs


devices = [
    {"id": 1, "name": "Projector", "status": "off", "total_usage_hours": 0},
    {"id": 2, "name": "Smart Light", "status": "off", "total_usage_hours": 3.5},
    {"id": 3, "name": "Fan", "status": "on", "total_usage_hours": 1.2},
]

def find_device_by_id(device_id):
    return next((device for device in devices if device["id"] == device_id), None)

def toggle_device_status(device_id, action):
    device = find_device_by_id(device_id)
    if device and action in ["on", "off"]:
        device["status"] = action
        logs.append({"device_id": device_id, "action": action})
        return {"message": f"Device '{device['name']}' turned {action}"}
    return {"error": "Invalid request"}