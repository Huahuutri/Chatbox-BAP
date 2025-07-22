import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load biến môi trường từ file .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "❗Bạn chưa nhập nội dung nào."})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Hoặc gpt-4 nếu có quyền
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI thân thiện."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        # Ghi log lỗi ra terminal để bạn dễ kiểm tra
        print("❌ Lỗi khi gọi OpenAI:", str(e))
        return jsonify({
            "reply": "🤖 Hệ thống AI đang được bảo trì & nâng cấp. Vui lòng liên hệ Zalo: "
                     "<a href='https://zalo.me/0916198819' target='_blank'>0916.19.88.19</a>. "
                     "Xin cảm ơn quý khách đã thông cảm!"
        }), 200  # Trả về 200 để không gây lỗi JS phía client

if __name__ == "__main__":
    app.run(debug=True)
