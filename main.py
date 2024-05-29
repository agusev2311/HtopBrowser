from flask import Flask, render_template, request
import os
import subprocess
# flask --app main run

def read_top_output():
    process = subprocess.Popen(['top', '-b', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        output = stdout.decode('utf-8')
        return output

class pr():
    def __init__(self, pid, tty, time, cmd):
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd

# def parse_top(top):
#     top_info = []
#     tasks_count = []
#     cpu = []
#     mem = []
#     swap = []
#     tasks = []
#     for i in range(len(top.split("\n"))):
#         if i == 0:


a = os.popen("ps", mode='r', buffering=-1)
b = ""
prs = []
for i in a.readlines()[1:]:
    pd, ty, tm, cd = i.split()
    prs += [pr(pid=pd, tty = ty, time = tm, cmd = cd)]
pd, ty, tm, cd = None, None, None, None
        
# b = a.read()  
print(b)

app = Flask(__name__)

@app.route("/")
def hello_world():
    top_output = read_top_output()
    b = ""
    for i in top_output.split("\n"):
        b += f"{i}<br/>"
    # return f"<p>Go to /hello/name?key=abc</p>"
    return f"<p>{b}<p>"

@app.route('/hello/')
@app.route('/hello/<name>/')
def hello(name=None):
    
    searchword = request.args.get('key', '')
    return render_template('hello.html', person=name, key=searchword, prs=prs)