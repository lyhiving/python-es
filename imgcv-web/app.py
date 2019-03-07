from flask import Flask, Response, request
import json
from core import find, upload

app = Flask('myApp')


@app.route('/')
def home():
    return 'success'


@app.route('/cv', methods=['POST'])
def start():
    file_path = upload.Upload().run(request)
    res = find.run(file_path, False)
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/cv/info', methods=['POST'])
def info():
    res = upload.Upload().file_info(request)
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
