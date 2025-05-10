import os
from flask import Flask, request, render_template, jsonify
from openai import OpenAI  # ★ v1 クライアント

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    text        = data.get("text", "")
    dialect     = data.get("dialect", "大阪弁")
    temperature = float(data.get("temperature", 0.3))   # ← スライダー値

    # ----- プロンプトを組み立て -----
    system_msg = (
        "あなたは優秀な日本語方言通訳です。"
        "語彙と語尾を自然に置き換えてください。"
        "意味が変わる場合は単語を置換しないでください。"
        "temperature は“ノリの強さ”を示し、高いほど自由に変換します。"
    )
    user_msg = f"標準語: {text}\n変換先方言: {dialect}\n→"

    # ----- OpenAI 呼び出し -----
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ],
        max_tokens=120,
        temperature=temperature
    )

    return jsonify({"result": resp.choices[0].message.content.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
