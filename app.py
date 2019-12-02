import json
import os
from Modules.learn import trainer
from Modules.send_data import save_data
from flask import Flask, render_template, request, send_from_directory, abort
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "Modules/data"

# TODO: add seesion handling

def add_to_csv(down, up):
   ### Merge down and up data together and add to time.csv
   with open('Modules/data/time.csv','a') as fd:
      for i in range(len(down)):
         fd.write(str(down[i]) + "," + str(up[i]))
         if (i != (len(down) - 1)):
            fd.write(",")
         else:
            fd.write("\n")

@app.route("/post_data", methods = ['POST'])
def get_post_data():
   ### Add the key-stroke timings to database
    print(request.remote_addr)
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    add_to_csv(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/post_test", methods = ['POST'])
def get_post_test():
   ### Authenticate the test
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    result = trainer(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
   ### Download the time.csv
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
   app.run(host= '0.0.0.0', debug='on')