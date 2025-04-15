from flask import jsonify


def success(message=None, data=None, status=200):
    response = {"success": True}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    return jsonify(response), status

def error(message="Щось пішло не так", errors=None, status=400):
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status
