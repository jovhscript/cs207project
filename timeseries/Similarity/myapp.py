from flask import Flask, request, render_template, jsonify
import find_most_similiar
from tstojson import *
# import server
import client
import os, shutil
application = Flask(__name__)

@application.route("/")
def home():
    return render_template('home.html')

@application.route("/search_index", methods=['GET', 'POST'])
def indb():
    return render_template("index.html")

@application.route("/search_index/results")
def search_index():
    i = request.args.get('id', 0, type=int)
    if i >= 1000:
        return jsonify(result='Invalid Index. Try again.')
    n = request.args.get('n', 0, type=int)
    print(i,n)
    res = client.fetch_byindex('Timeseries'+str(i), n)
    print(res)
    return jsonify(result=res)

@application.route("/search_meta")
def meta():
    return render_template('meta.html')

@application.route("/search_upload")
def upload():
    return render_template('upload.html')

@application.route("/search_upload/results", methods=['GET', 'POST'])
def search_upload():
    if request.method == 'POST':
        f=request.files['ts']
        os.mkdir('tmp/')
        f.save('tmp/'+f.filename)
        res = client.fetch_upload('tmp/'+f.filename, 1)
        shutil.rmtree('tmp/')
        # print('<p>'+str(res)+'</p>')
    return render_template('upload.html', output=res)
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)