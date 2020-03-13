import json
import os
import random
import string
import requests

from Modules.learn import tester
from Modules.utils import session_number, add_to_csv
from flask import Flask, render_template, request, send_from_directory, abort, jsonify
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "Modules/data"

# TODO: add seesion handling


@app.route("/post_data", methods=['POST'])
def get_post_data():
    # Add the key-stroke timings to database
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    add_to_csv(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/post_test", methods=['POST'])
def get_post_test():
    # Authenticate the test
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    result = tester(json.loads(js_d_data), json.loads(js_u_data))
    return jsonify(result=result)

@app.route('/upload/<path:filename>', methods=['POST'])
# Upload the time.csv
def upload(filename):
    # uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if os.path.exists("Modules/data/time.csv"):
        hash_name = "".join( [random.choice(string.ascii_letters) for i in range(6)] )
        data=open("Modules/data/time.csv", 'rb')
        requests.put("http://s3-eu-central-1.amazonaws.com/ucontacti/keystroke/" + "time_" + hash_name + ".csv",
            data=data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return jsonify(status="file not exist")

@app.route("/del_data", methods=['POST'])
def del_post():
    # Delete current data
    if os.path.exists("Modules/data/time.csv"):
        os.remove("Modules/data/time.csv")
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/init", methods=['POST'])
def init_client():
    # Init client status
    if os.path.exists("Modules/data/time.csv"):
        result = session_number()
    else:
        result = 0
    return jsonify(session=result)


@app.route('/download/<path:filename>', methods=['POST'])
# Download the time.csv
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if os.path.exists("Modules/data/time.csv"):
        return send_from_directory(directory=uploads, filename=filename), 200
    else:
        return jsonify(status="file not exist")



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='on')
