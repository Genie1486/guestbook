from flask import Flask, request, redirect, render_template
import json
import os
import redis

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "guestbook.json")

PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
MODE = os.getenv('MODE', 'production')

# ✅ Redis 연결 추가!
r = redis.Redis(
    host='redis',            # ← 서비스명으로 연결
    port=6379,
    decode_responses=True    # ← 문자열 자동 변환
)

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_entries(entries):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, ensure_ascii=False)

@app.route("/", methods=["GET"])
def index():
    # ✅ 방문자 수 Redis로 카운트!
    visit_count = r.incr("visit_count")
    entries = load_entries()
    return render_template("index.html", entries=entries, visit_count=visit_count)

@app.route("/write", methods=["POST"])
def write():
    name = request.form.get("name", "익명")
    message = request.form.get("message", "")

    if message:
        entries = load_entries()
        entries.append({"name": name, "message": message})
        save_entries(entries)

    return redirect("/")

@app.route("/health")
def health():
    # ✅ Redis 상태도 함께 체크!
    try:
        r.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"

    return {"status": "ok", "redis": redis_status}, 200

if __name__ == "__main__":
    print(f"🚀 Starting app in {MODE} mode on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)