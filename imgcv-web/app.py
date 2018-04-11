from flask import Flask, Response, request
import json
import uuid
import core.find as find

app = Flask('myApp')


@app.route('/')
def home():
    return 'success'


@app.route('/cv', methods=['POST'])
def start():
    f = request.files['file']
    # number = request.form['number']
    filename = f.filename
    file_types = filename.split(".")
    file_type = filename.split(".")[len(file_types) - 1]
    file_path = './static/' + str(uuid.uuid1()) + '.' + file_type
    f.save(file_path)
    # print(number)
    res = find.run(file_path, False)
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
