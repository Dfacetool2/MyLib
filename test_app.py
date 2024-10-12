import unittest
import json
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello, World!')

    def test_calculate_hypotenuse_success(self):
        payload = {
            'a': 3,
            'b': 4
        }
        response = self.app.post('/calculate-hypotenuse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['a'], 3.0)
        self.assertEqual(data['b'], 4.0)
        self.assertEqual(data['c'], 5.0)

    def test_calculate_hypotenuse_missing_fields(self):
        # 测试缺少字段
        payload = {
            'a': 3
        }
        response = self.app.post('/calculate-hypotenuse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'JSON 数据中必须包含 "a" 和 "b" 两个字段')

    def test_calculate_hypotenuse_non_numeric(self):
        # 测试非数字输入
        payload = {
            'a': 'three',
            'b': 4
        }
        response = self.app.post('/calculate-hypotenuse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], '"a" 和 "b" 必须是数字')

    def test_calculate_hypotenuse_negative_numbers(self):
        # 测试负数输入
        payload = {
            'a': -3,
            'b': 4
        }
        response = self.app.post('/calculate-hypotenuse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], '"a" 和 "b" 必须是正数')

    def test_calculate_hypotenuse_zero_values(self):
        # 测试零值输入
        payload = {
            'a': 0,
            'b': 4
        }
        response = self.app.post('/calculate-hypotenuse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], '"a" 和 "b" 必须是正数')

    def test_calculate_hypotenuse_invalid_json(self):
        # 测试无效的 JSON 数据
        invalid_json = "This is not JSON"
        response = self.app.post('/calculate-hypotenuse',
                                 data=invalid_json,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], '请求体中必须包含 JSON 数据')

if __name__ == '__main__':
    unittest.main()
