from flask import Flask, render_template, request
import os

class pr():
    def __init__(self, pid, tty, time, cmd):
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd

a = os.popen("ps", mode='r', buffering=-1)
b = ""
prs = []
for i in a.readlines()[1:]:
    pd, ty, tm, cd = i.split()
    prs += [pr(pid=pd, tty = ty, time = tm, cmd = cd)]
        
# b = a.read()  
print(b)

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return f"<p>{b}</p>"



@app.route('/hello/')
@app.route('/hello/<name>/')
def hello(name=None):
    searchword = request.args.get('key', '')
    return render_template('hello.html', person=name, key=searchword, prs=prs)