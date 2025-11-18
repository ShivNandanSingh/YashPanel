from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Allow Vue dev server
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5173"]
)

# In-memory storage (resets on restart)
users = []
services = [
    {
        "id": "svc_instagram_followers",
        "name": "Instagram Followers",
        "description": "Mock Instagram followers (demo only).",
        "ratePer1000": 50,
        "status": "active"
    },
    {
        "id": "svc_youtube_views",
        "name": "YouTube Views",
        "description": "Mock YouTube views (demo only).",
        "ratePer1000": 30,
        "status": "active"
    },
    {
        "id": "svc_instagram_likes",
        "name": "Instagram Likes",
        "description": "Mock Instagram likes (demo only).",
        "ratePer1000": 20,
        "status": "active"
    },
]
orders = []

# Create default admin user
def create_admin_if_not_exists():
    global users
    admin_email = "admin@example.com"
    for u in users:
        if u["email"].lower() == admin_email.lower():
            return
    admin_user = {
        "id": str(uuid.uuid4()),
        "name": "Admin",
        "email": admin_email,
        "passwordHash": generate_password_hash("Admin@123"),
        "balance": 0.0,
        "isAdmin": True,
    }
    users.append(admin_user)

create_admin_if_not_exists()


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def login_required(f):
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs, current_user=user)
    wrapper.__name__ = f.__name__
    return wrapper


def admin_required(f):
    @login_required
    def wrapper(*args, **kwargs):
        current_user = kwargs.pop("current_user")
        if not current_user.get("isAdmin"):
            return jsonify({"error": "Forbidden"}), 403
        return f(*args, **kwargs, current_user=current_user)
    wrapper.__name__ = f.__name__
    return wrapper


def public_user_data(u):
    return {
        "id": u["id"],
        "name": u["name"],
        "email": u["email"],
        "balance": u["balance"],
        "isAdmin": u["isAdmin"],
    }


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    # very simple email check
    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    # Check if email exists
    for u in users:
        if u["email"].lower() == email:
            return jsonify({"error": "Email already registered"}), 400

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "passwordHash": generate_password_hash(password),
        "balance": 0.0,
        "isAdmin": False,
    }
    users.append(new_user)
    return jsonify({"message": "Registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    for u in users:
        if u["email"].lower() == email:
            if check_password_hash(u["passwordHash"], password):
                session["user_id"] = u["id"]
                return jsonify({"user": public_user_data(u)})
            else:
                return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})


@app.route("/api/me", methods=["GET"])
def me():
    user = get_current_user()
    if not user:
        return jsonify({"user": None}), 200
    return jsonify({"user": public_user_data(user)}), 200


@app.route("/api/services", methods=["GET"])
def list_services():
    active = [s for s in services if s["status"] == "active"]
    return jsonify({"services": active})


@app.route("/api/orders", methods=["GET"])
@login_required
def list_orders(current_user):
    user_orders = [o for o in orders if o["userId"] == current_user["id"]]
    return jsonify({"orders": user_orders})


@app.route("/api/orders", methods=["POST"])
@login_required
def create_order(current_user):
    data = request.get_json() or {}
    service_id = data.get("serviceId")
    quantity = data.get("quantity")
    target = (data.get("target") or "").strip()

    if not service_id or not quantity or not target:
        return jsonify({"error": "serviceId, quantity and target are required"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Quantity must be an integer"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400

    svc = None
    for s in services:
        if s["id"] == service_id and s["status"] == "active":
            svc = s
            break

    if not svc:
        return jsonify({"error": "Invalid service"}), 400

    total_price = (svc["ratePer1000"] * quantity) / 1000.0

    if current_user["balance"] < total_price:
        return jsonify({"error": "Insufficient balance"}), 400

    # Deduct balance
    current_user["balance"] -= total_price

    order = {
        "id": str(uuid.uuid4()),
        "userId": current_user["id"],
        "serviceId": svc["id"],
        "serviceName": svc["name"],
        "quantity": quantity,
        "target": target,
        "totalPrice": total_price,
        "status": "pending",
        "createdAt": datetime.utcnow().isoformat() + "Z",
    }
    orders.append(order)
    return jsonify({"order": order, "balance": current_user["balance"]}), 201


@app.route("/api/orders/simulate", methods=["POST"])
@login_required
def simulate_order(current_user):
    pending = [o for o in orders if o["userId"] == current_user["id"] and o["status"] == "pending"]
    if not pending:
        return jsonify({"message": "No pending orders to process"}), 200
    order = random.choice(pending)
    order["status"] = "completed"
    return jsonify({"order": order}), 200


# Admin endpoints
@app.route("/api/admin/users", methods=["GET"])
@admin_required
def admin_users(current_user):
    return jsonify({"users": [public_user_data(u) for u in users]})


@app.route("/api/admin/orders", methods=["GET"])
@admin_required
def admin_orders(current_user):
    return jsonify({"orders": orders})


@app.route("/api/admin/orders/<order_id>", methods=["PATCH"])
@admin_required
def admin_update_order(current_user, order_id):
    data = request.get_json() or {}
    status = data.get("status")
    if status not in ["pending", "processing", "completed", "cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    for o in orders:
        if o["id"] == order_id:
            o["status"] = status
            return jsonify({"order": o}), 200

    return jsonify({"error": "Order not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
