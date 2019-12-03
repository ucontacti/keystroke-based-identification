import json
import os
from Modules.learn import trainer
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
    result = trainer(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


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
    try:
        return send_from_directory(directory=uploads, filename=filename)
    except FileNotFoundError:
        abort(404)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='on')
