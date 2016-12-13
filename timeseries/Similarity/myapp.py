from flask import Flask, request, render_template, jsonify
import find_most_similiar
from tstojson import *
import client
import os, shutil
application = Flask(__name__)

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
        i = request.args.get('id', '0', type=str)
        if i.isdigit():
            i = int(i)
        else:
            raise InvalidUsage('Index must be a integer', status_code=400)
        n = request.args.get('n', '1', type=str)
        if n.isdigit():
            n = int(n)
        else:
            print('here')
            raise InvalidUsage('Number of neighbours must be a integer', status_code=400)
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

@application.route("/meta")
def meta():
    return render_template('meta.html')

@application.route('/meta/', methods=['GET'])
def get_all_meta():
    return jsonify(result='all')

@application.route('/meta/filter', methods=['GET'])
def filter_meta():
    ls = request.args.get('levels', None, type=str)
    ls_flag = False
    ms = request.args.get('mean_range', None, type=str)
    ms_flag = False
    stds = request.args.get('std_range', None, type=str)
    std_flag = False
    
    if ls != '':
        ls = ls.split(',')
        ls_flag=True

    if ms != '':
        try:
            ms = [float(x) for x in ms.split('-')]
            ms_flag = True
        except:
            raise InvalidUsage('Mean boundaries should be convertible to floats', status_code=400)

    if ls_flag and ms_flag:
        raise InvalidUsage('Select only one filter at a time', status_code=400)

    if stds != '':
        try:
            stds = [float(x) for x in stds.split('-')]
            std_flag = True
        except:
            raise InvalidUsage('Std boundaries should be convertible to floats', status_code=400)

    if (ls_flag and std_flag) or (ms_flag and std_flag):
        raise InvalidUsage('Select only one filter at a time', status_code=400)
    res = [ls, ms, stds]
    return jsonify(result=res)

@application.route('/meta/', methods=['POST'])
def add_ts():
    f=request.files['ts']
    if f.filename[-4:] != 'json':
        raise InvalidUsage('Invalid File Type Supplied', status_code=400)
    try:
        shutil.rmtree('tmp/')
    except:
        os.mkdir('tmp/')
    f.save('tmp/'+f.filename)
    shutil.rmtree('tmp/')
    return jsonify(result=f.filename)

@application.route('/meta/<int:id>', methods=['GET'])
def get_ts(id):
    if not isinstance(id, int):
        raise InvalidUsage('Number of neighbours must be a integer', status_code=400)
    # return task_db.fetch_task(id)
    return jsonify(result=id)
    # @application.route("/meta")

    # return render_template('upload.html', output=res)
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)