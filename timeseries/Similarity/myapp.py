from flask import Flask, request, render_template
import find_most_similiar
from tstojson import *
# import server
import client
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template('home.html')

@application.route("/search_index", methods=['GET', 'POST'])
def indb():
    html = "<h1 style='color:blue'>Choose the index of the Timeseries !</h1>"
    html += '<form action="/search_index/results" method="post"><select name="id"><option value="0">Timeseries 0</option><option value="1">Timeseries 1</option></select>'
    # html += "<button type='button'><a href='/search_index/results'>Search for Timeseries0</a></button>"
    html += '<input class="SubmitButton" type="submit" name="SUBMITBUTTON"  value="Submit" style="font-size:20px; " /></form>'
    return html
@application.route("/search_index/results", methods=['GET','POST'])
def search_index():
    print(request.method)
    if request.method == 'POST':
        res = client.fetch('Timeseries'+str(request.form['id']), 1)
        return '<p>'+str(res)+'</p>'

@application.route("/search_meta")
def meta():
    return render_template('meta.html')

@application.route("/search_upload")
def upload():
    return render_template('upload.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)