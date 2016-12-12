from flask import Flask, request, render_template, jsonify
#from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
import find_most_similiar
from tstojson import *
# import server
import client
import os, shutil
application = Flask(__name__)

## set up db configuration
#user = "cs207"
#password = "cs207password"
#host = "localhost"
##port = "5432"
#db = "ts_postgres"
#url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
#application.config['SQLALCHEMY_DATABASE_URI'] = url
#db = SQLAlchemy(application)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    # return render_template('error.html', output='BLA')
    return response

@application.route("/")
def home():
    return render_template('home.html')

@application.route("/simsearch", methods=['GET', 'POST'])
def indb():
    return render_template("index.html")

@application.route("/simsearch/", methods=['GET', 'POST'])
def search_index():
    if request.method == 'GET':
        i = request.args.get('id', 0, type=int)
        n = request.args.get('n', 0, type=int)
        res = client.fetch_byindex('Timeseries'+str(i), n+1)
    elif request.method == 'POST':
        # print(request.form.getlist('ts'))
        f=request.files['ts']
        n=int(request.values['Number'])
        print(f, n)
        if f.filename[-4:] != 'json':
            raise InvalidUsage('Invalid File Type Supplied', status_code=400)
        try:
            shutil.rmtree('tmp/')
        except:
            os.mkdir('tmp/')
        f.save('tmp/'+f.filename)
        res = client.fetch_upload('tmp/'+f.filename, n)
        shutil.rmtree('tmp/')
        print(res)
    if 'ERROR' in res:
        raise InvalidUsage(res, status_code=400)
    return jsonify(result=res)

@application.route("/search_meta/")
def meta():
    return render_template('meta.html')

@application.route("/search_meta/id", methods=['GET'])
def search_meta1():
    return sencode('Timeseries0.json')

    # return render_template('upload.html', output=res)
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)