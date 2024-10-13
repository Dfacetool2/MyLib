from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
import math

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/calculate-hypotenuse', methods=['POST'])
def calculate_hypotenuse():
    """
    计算直角三角形的斜边。

    请求:
        POST /calculate-hypotenuse
        Content-Type: application/json
        {
            "a": 3,
            "b": 4
        }

    响应:
        {
            "a": 3,
            "b": 4,
            "c": 5
        }
    """
    try:
        # 获取 JSON 数据
        data = request.get_json()
    except BadRequest:
        return jsonify({'error': '请求体中必须包含有效的 JSON 数据'}), 400

    # 验证输入数据
    if not data:
        return jsonify({'error': '请求体中必须包含 JSON 数据'}), 400

    if 'a' not in data or 'b' not in data:
        return jsonify({'error': 'JSON 数据中必须包含 "a" 和 "b" 两个字段'}), 400

    try:
        a = float(data['a'])
        b = float(data['b'])

        if a <= 0 or b <= 0:
            return jsonify({'error': '"a" 和 "b" 必须是正数'}), 400

    except (ValueError, TypeError):
        return jsonify({'error': '"a" 和 "b" 必须是数字'}), 400

    # 计算斜边
    c = math.sqrt(a ** 2 + b ** 2)

    # 返回结果
    return jsonify({
        'a': a,
        'b': b,
        'c': round(c, 2)  # 保留两位小数
    })

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'error': '请求体中必须包含有效的 JSON 数据'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
