from flask import Flask, request, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
import find_most_similiar
from tstojson import *
# import server
import client
import os, shutil
application = Flask(__name__)

# set up db configuration
user = "cs207"
password = "cs207password"
host = "localhost"
port = "5432"
db = "ts_postgres"
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
application.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(application)


@application.route("/")
def home():
    return render_template('home.html')

@application.route("/search_index/", methods=['GET', 'POST'])
def indb():
    return render_template("index.html")

@application.route("/search_index/results")
def search_index():
    i = request.args.get('id', 0, type=int)
    if i >= 1000:
        return jsonify(result='Invalid Index. Try again.')
    n = request.args.get('n', 0, type=int)
    print(i,n)
    res = client.fetch_byindex('Timeseries'+str(i), n+1)
    print(type(res))
    return jsonify(result=res)

@application.route("/search_meta/")
def meta():
    return render_template('meta.html')

@application.route("/search_meta/id", methods=['GET'])
def search_meta1():
    return sencode('Timeseries0.json')

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