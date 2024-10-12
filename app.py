from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/calculate-hypotenuse', methods=['POST'])
def calculate_hypotenuse():
    """

    request:
        POST /calculate-hypotenuse
        Content-Type: application/json
        {
            "a": 3,
            "b": 4
        }

    reply:
        {
            "a": 3,
            "b": 4,
            "c": 5
        }
    """
    # get json
    data = request.get_json()

    # vadidate input
    if not data:
        return jsonify({'error': '请求体中必须包含 JSON 数据'}), 400

    if 'a' not in data or 'b' not in data:
        return jsonify({'error': 'JSON 数据中必须包含 "a" 和 "b" 两个字段'}), 400

    try:
        a = float(data['a'])
        b = float(data['b'])

        if a <= 0 or b <= 0:
            return jsonify({'error': '"a" 和 "b" 必须是正数'}), 400

    except ValueError:
        return jsonify({'error': '"a" 和 "b" 必须是数字'}), 400

    # caculate
    c = math.sqrt(a ** 2 + b ** 2)

    return jsonify({
        'a': a,
        'b': b,
        'c': round(c, 2)  # keep two decimal
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
