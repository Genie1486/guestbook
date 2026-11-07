from flask import Flask, request, redirect, render_template
import json
import os

app = Flask(__name__)

# ✅ __file__ 기준으로 경로 설정 (하드코딩 제거!)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "guestbook.json")


def load_entries():
    """방명록 데이터 불러오기"""
    if not os.path.exists(DATA_FILE):
        return []
    try:  # ✅ 빈 파일 예외처리 추가!
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_entries(entries):
    """방명록 데이터 저장하기"""
    os.makedirs(DATA_DIR, exist_ok=True)  # ✅ 하드코딩 제거!
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, ensure_ascii=False)


@app.route("/", methods=["GET"])
def index():
    """메인 페이지 - 방명록 목록 보여주기"""
    entries = load_entries()
    return render_template("index.html", entries=entries)


@app.route("/write", methods=["POST"])
def write():
    """방명록 글 저장하기"""
    name = request.form.get("name", "익명")
    message = request.form.get("message", "")

    if message:
        entries = load_entries()
        entries.append({"name": name, "message": message})
        save_entries(entries)

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
