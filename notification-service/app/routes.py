from flask import Blueprint, request, jsonify

from flask import Blueprint, jsonify

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "service": "notification-service"}), 200


notify_routes = Blueprint('notify_routes', __name__)

@notify_routes.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Notification Service is running"}), 200

@notify_routes.route('/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    user = data.get("user", "Unknown")
    message = data.get("message", "No message provided")

    # Тут буде імітація відправки email
    print(f"[NOTIFY] 📬 Для користувача {user}: {message}")

    return jsonify({"status": "success", "info": f"Notification sent to {user}"}), 200
