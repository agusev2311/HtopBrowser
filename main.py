from flask import Flask, render_template, request
import os
import subprocess
from bs4 import BeautifulSoup
# flask --app main run
# flask --app main run --debug --host 0.0.0.0

def read_top_output():
    process = subprocess.Popen(['top', '-b', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        output = stdout.decode('utf-8')
        return output

def read_htop_output():
    return os.popen("sleep 1; echo q | htop | aha --black --line-fix").read()

class pr():
    def __init__(self, pid, tty, time, cmd):
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd

class pr_top():
    def __init__(self, pid, user, pr, ni, virt, res, shr, s, cpu, mem, time, command):
        self.pid = pid
        self.user = user
        self.pr = pr
        self.ni = ni
        self.virt = virt
        self.res = res
        self.shr = shr
        self.s = s
        self.cpu = cpu
        self.mem = mem
        self.time = time
        self.command = command

def parse_top(top):
    top_info = []
    tasks_count = []
    cpu = []
    mem = []
    swap = []
    tasks = []
    for i in range(len(top.split("\n"))):
        j = top.split("\n")[i].split()
        if i == 0:
            top_info += [j[2], j[4], j[5], j[9], j[10], j[11]]
        elif i == 1:
            tasks_count += [j[1], j[3], j[5], j[7], j[9]]
        elif i == 2:
            cpu += [j[1], j[3], j[5], j[7], j[9], j[11], j[13], j[15]]
        elif i == 3:
            mem += [j[3], j[5], j[7], j[9]]
        elif i == 4:
            swap += [j[2], j[4], j[6], j[8]]
        elif i in [5, 6, len(top.split("\n")) - 1]:
            pass
        else:
            task_top = pr_top(j[0], j[1], j[2], j[3], 
                              j[4], j[5], j[6], j[7], 
                              j[8], j[9], j[10], j[11])
            tasks += [task_top]
    task_top = None
    return [top_info, tasks_count, cpu, mem, swap, tasks]

def parse_htop(htop):
    soup = BeautifulSoup(htop, 'html.parser')
    return soup.prettify()
def htop_cpu(htop):
    soup = BeautifulSoup(htop, 'html.parser')
    # soup.find(text='span style="font-weight:bold;filter: contrast(70%) brightness(190%);color:dimgray;"')
    target_spans = soup.find_all('span', style="font-weight:bold;filter: contrast(70%) brightness(190%);color:dimgray;")
    contents = [span.text.strip() for span in target_spans]
    contents2 = []
    for i in contents:
        if "%" in i:
            contents2.append(i)
    return contents2

print(read_top_output())
                     
app = Flask(__name__)

@app.route("/")
def hello_world():
    top_output = read_top_output()
    b = ""
    for i in top_output.split("\n"):
        b += f"{i}<br/>"
    # return f"<p>Go to /hello/name?key=abc</p>"
    return f"<p>{b}<p/>"

@app.route("/table_css")
def ret_table_css():
    top_parse = parse_top(read_top_output())
    return render_template('table_css.html', prs=top_parse[5])

@app.route('/index/')
def index():
    top_parse = parse_top(read_top_output())
    return render_template('index.html', prs=top_parse[5])

@app.route("/table")
def ret_table():
    return render_template('table.html', prs=parse_htop(read_htop_output()))

@app.route('/hello/')
def hello():
    return render_template('hello.html', prs=parse_htop(read_htop_output()))

# parse_top(read_top_output())
# print(htop_cpu(read_htop_output()))