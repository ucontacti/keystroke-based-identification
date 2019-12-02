import json
import os
from Modules.learn import trainer
from Modules.send_data import save_data
from flask import Flask, render_template, request, send_from_directory, abort
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "Modules/data"


def add_to_csv(down, up):
   with open('Modules/data/time.csv','a') as fd:
      for i in range(len(down)):
         fd.write(str(down[i]) + "," + str(up[i]))
         if (i != (len(down) - 1)):
            fd.write(",")
         else:
            fd.write("\n")

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/post_data", methods = ['POST'])
def get_post_data():
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    add_to_csv(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/post_test", methods = ['POST'])
def get_post_test():
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    result = trainer(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# @app.route("/post_send_data", methods = ['POST'])
# def get_post_send_data():
#     result = save_data()
#     return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    print(filename)
    return send_from_directory(directory=uploads, filename=filename)

# @app.route("/get-csv/<csv_id>")
# def get_csv(csv_id):

#     filename = f"{csv_id}.csv"
#     print(filename)
#     print(app.config["CLIENT_CSV"])
#     try:
#         return send_from_directory(app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)

if __name__ == '__main__':
   app.run(host= '0.0.0.0', debug='on')