from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Allow CORS
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5173",
        "https://yashpanel-frontend.vercel.app",  # your real Vercel URL
    ]
)


# JSON file paths
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"


# ------------------------
# JSON LOAD / SAVE HELPERS
# ------------------------

def load_json(filename, default):
    if not os.path.exists(filename):
        save_json(filename, default)
        return default
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


# ------------------------
# Load data on server start
# ------------------------

users = load_json(USERS_FILE, [])
orders = load_json(ORDERS_FILE, [])

# Hard-coded services
services = [
    {
        "id": "svc_instagram_followers",
        "name": "Instagram Followers",
        "description": "Mock Instagram followers (demo).",
        "ratePer1000": 50,
        "status": "active"
    },
    {
        "id": "svc_youtube_views",
        "name": "YouTube Views",
        "description": "Mock YouTube views (demo).",
        "ratePer1000": 30,
        "status": "active"
    },
    {
        "id": "svc_instagram_likes",
        "name": "Instagram Likes",
        "description": "Mock Instagram likes (demo).",
        "ratePer1000": 20,
        "status": "active"
    },
]


# ------------------------
# Create admin if missing
# ------------------------

def create_admin_if_not_exists():
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
    save_json(USERS_FILE, users)


create_admin_if_not_exists()


# ------------------------
# Helper functions
# ------------------------

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def public_user_data(u):
    return {
        "id": u["id"],
        "name": u["name"],
        "email": u["email"],
        "balance": u["balance"],
        "isAdmin": u["isAdmin"],
    }


def login_required(f):
    def wrapper(*args, **kwargs):
        u = get_current_user()
        if not u:
            return jsonify({"error": "Unauthorized"}), 401
        return f(current_user=u, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def admin_required(f):
    @login_required
    def wrapper(current_user, *args, **kwargs):
        if not current_user["isAdmin"]:
            return jsonify({"error": "Forbidden"}), 403
        return f(current_user=current_user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


# ------------------------
# AUTH ENDPOINTS
# ------------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

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
    save_json(USERS_FILE, users)

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
    u = get_current_user()
    if not u:
        return jsonify({"user": None})
    return jsonify({"user": public_user_data(u)})


# ------------------------
# SERVICES & ORDERS
# ------------------------

@app.route("/api/services", methods=["GET"])
def get_services():
    return jsonify({"services": services})


@app.route("/api/orders", methods=["GET"])
@login_required
def get_orders(current_user):
    my_orders = [o for o in orders if o["userId"] == current_user["id"]]
    return jsonify({"orders": my_orders})


@app.route("/api/orders", methods=["POST"])
@login_required
def create_order(current_user):
    data = request.get_json() or {}
    service_id = data.get("serviceId")
    quantity = data.get("quantity")
    target = (data.get("target") or "").strip()

    if not service_id or not quantity or not target:
        return jsonify({"error": "All fields required"}), 400

    try:
        quantity = int(quantity)
    except:
        return jsonify({"error": "Quantity must be number"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400

    svc = next((s for s in services if s["id"] == service_id), None)
    if not svc:
        return jsonify({"error": "Invalid service"}), 400

    total = (svc["ratePer1000"] * quantity) / 1000.0

    if current_user["balance"] < total:
        return jsonify({"error": "Insufficient balance"}), 400

    current_user["balance"] -= total

    order = {
        "id": str(uuid.uuid4()),
        "userId": current_user["id"],
        "serviceId": svc["id"],
        "serviceName": svc["name"],
        "quantity": quantity,
        "target": target,
        "totalPrice": total,
        "status": "pending",
        "createdAt": datetime.utcnow().isoformat() + "Z",
    }

    orders.append(order)

    save_json(USERS_FILE, users)
    save_json(ORDERS_FILE, orders)

    return jsonify({"order": order, "balance": current_user["balance"]})


@app.route("/api/orders/simulate", methods=["POST"])
@login_required
def simulate(current_user):
    pending = [o for o in orders if o["userId"] == current_user["id"] and o["status"] == "pending"]
    if not pending:
        return jsonify({"message": "No pending orders"})

    order = random.choice(pending)
    order["status"] = "completed"

    save_json(ORDERS_FILE, orders)

    return jsonify({"order": order})


# ------------------------
# ADMIN
# ------------------------

@app.route("/api/admin/users", methods=["GET"])
@admin_required
def admin_users(current_user):
    return jsonify({"users": users})


@app.route("/api/admin/orders", methods=["GET"])
@admin_required
def admin_all_orders(current_user):
    return jsonify({"orders": orders})


@app.route("/api/admin/orders/<order_id>", methods=["PATCH"])
@admin_required
def admin_update_order(current_user, order_id):
    data = request.get_json() or {}
    new_status = data.get("status")

    for o in orders:
        if o["id"] == order_id:
            o["status"] = new_status
            save_json(ORDERS_FILE, orders)
            return jsonify({"order": o})

    return jsonify({"error": "Order not found"}), 404


# ------------------------
# RUN SERVER
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
