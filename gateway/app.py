from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Проксі до auth-service
@app.route('/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path):
    response = requests.request(
        method=request.method,
        url=f'http://auth-service:8000/{path}',
        headers={key: value for (key, value) in request.headers},
        json=request.get_json(silent=True)
    )
    return (response.text, response.status_code, response.headers.items())

# Проксі до user-service
@app.route('/users/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_proxy(path):
    response = requests.request(
        method=request.method,
        url=f'http://user-service:8001/{path}',
        headers={key: value for (key, value) in request.headers},
        json=request.get_json(silent=True)
    )
    return (response.text, response.status_code, response.headers.items())

# Головна сторінка
@app.route('/')
def index():
    return jsonify({"message": "Gateway is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
