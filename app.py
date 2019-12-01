import json
from flask import Flask, render_template, request
app = Flask(__name__)

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

@app.route("/postmethod", methods = ['POST'])
def get_post_javascript_data():
    js_d_data = request.form['down_time_data']
    js_u_data = request.form['up_time_data']
    add_to_csv(json.loads(js_d_data), json.loads(js_u_data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
   app.run(host= '0.0.0.0', debug='on')