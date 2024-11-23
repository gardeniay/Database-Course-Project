from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# 高德地图API的key
key = 'd6efac766b1b06f5b36a8dbe10a17fd5'


# 获取地理编码
def get_code(address: str):
    parameters = {'key': key, 'address': address}
    res = requests.get("https://restapi.amap.com/v3/geocode/geo", params=parameters)
    jd = res.json()
    if 'geocodes' in jd and len(jd['geocodes']) > 0:
        return jd['geocodes'][0]['location']
    return None


@app.route('/')
def index():
    """加载主页"""
    return render_template('index.html')


@app.route('/plan_route', methods=['POST'])
def plan_route():
    """规划路线接口"""
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    if not origin or not destination:
        return jsonify({'success': False, 'message': '请提供有效的出发点和目的地'})

    code1 = get_code(origin)
    code2 = get_code(destination)

    if code1 and code2:
        # 调用高德地图步行路线规划API
        url = f'https://restapi.amap.com/v3/direction/walking?key={key}&origin={code1}&destination={code2}'
        response = requests.get(url)
        route_data = response.json()

        if route_data['status'] == '1' and 'paths' in route_data['route']:
            route = route_data['route']['paths'][0]
            duration = route['duration']
            return jsonify({
                'success': True,
                'duration': int(duration) // 60,
                'map_url': f"https://www.amap.com/search?query={origin}至{destination}&city="
            })
        else:
            return jsonify({'success': False, 'message': '路线规划失败，请检查输入的地址'})

    return jsonify({'success': False, 'message': '地理编码获取失败，请检查输入的地址'})


if __name__ == '__main__':
    app.run(debug=True)
