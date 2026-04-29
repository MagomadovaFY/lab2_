from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "username": "ivanov", "email": "ivanov@example.com"},
    {"id": 2, "username": "petrova", "email": "petrova@example.com"}
]
next_id = 3

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"users": users})

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.json
    if not data or not data.get("username") or not data.get("email"):
        return jsonify({"error": "username and email are required"}), 400
    new_user = {
        "id": next_id,
        "username": data["username"],
        "email": data["email"]
    }
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)