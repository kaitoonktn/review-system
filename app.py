"""
レビュー生成Webアプリ
Flask + review_engine.py で動作
"""

from flask import Flask, render_template, request, jsonify
from review_engine import generate_review, STYLES

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    product_name = data.get("product_name", "").strip()
    points_raw   = data.get("points", "").strip()
    style_key    = data.get("style", "2")   # デフォルト：カジュアル
    format_key   = data.get("format", "1")  # デフォルト：Amazon風

    # バリデーション
    if not product_name:
        return jsonify({"error": "商品名を入力してください"}), 400

    # ポイントを行ごとに分割・空行除去
    points = [p.strip() for p in points_raw.splitlines() if p.strip()]
    if not points:
        return jsonify({"error": "レビューポイントを1つ以上入力してください"}), 400

    # スタイルキーのバリデーション
    if style_key not in STYLES:
        style_key = "2"

    style = STYLES[style_key]
    result = generate_review(product_name, points, style)

    return jsonify({
        "title":  result["title"],
        "body":   result["body"],
        "stars":  result["stars"],
        "period": result["period"],
        "style":  result["style"],
    })


if __name__ == "__main__":
    # host="0.0.0.0" にするとスマホからもアクセス可能（同一Wi-Fi）
    app.run(debug=True, host="0.0.0.0", port=5000)
