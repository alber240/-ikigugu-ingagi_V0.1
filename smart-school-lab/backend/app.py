from flask import Flask, request
from flask_cors import CORS

# ✅ Import Blueprints
from controllers.device_controller import device_bp
from controllers.user_controller import user_bp
from controllers.log_controller import log_bp
from controllers.auth_controller import auth_bp  # ✅ Add authentication blueprint

app = Flask(__name__)

# ✅ Apply CORS globally
CORS(app, resources={r"/*": {
    "origins": "*", 
    "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"], 
    "allow_headers": ["Content-Type", "Authorization"]
}})

# ✅ Register Blueprints
app.register_blueprint(device_bp, url_prefix="/devices")
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(log_bp, url_prefix="/logs")
app.register_blueprint(auth_bp, url_prefix="/auth")  # ✅ Register authentication routes

# ✅ Handle OPTIONS requests globally
@app.before_request
def handle_options_request():
    """ Handles preflight OPTIONS requests globally for CORS compliance """
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

# ✅ Start Flask application
if __name__ == '__main__':
    app.run(debug=True)
