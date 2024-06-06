from flask import Flask, render_template, request, send_from_directory
import flask
import os
import subprocess
from bs4 import BeautifulSoup
import psutil
import jwt

app = flask.Flask(__name__)
app.secret_key = open("secret_key", "r").readlines()[0]

# flask --app main run
# flask --app main run --debug --host 0.0.0.0

users = {}

for i in open("users", "r").readlines():
    users[i.split()[0]] = {"password": i.split()[1]}

def kill_process(process_id):
    try:
        subprocess.call(['kill', '-9', str(process_id)])
        return "Ok"
    except:
        return "<i>Failed :(<i>"

def read_top_output():
    process = subprocess.Popen(['top', '-b', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        output = stdout.decode('utf-8')
        return output

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
            mem += [float(j[3]), float(j[5]), j[7], j[9]]
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

def cpu_usage():
    cpu_percents2 = psutil.cpu_percent(percpu=True)
    cpu_percents = []
    for i in cpu_percents2:
        cpu_percents.append([i])
    if len(cpu_percents2) > 7:
        if len(cpu_percents2) <= 24:
            if len(cpu_percents2) % 2 == 0 and len(cpu_percents2) // 2 <= 8:
                cpu_percents = []
                for i in range(len(cpu_percents2) // 2):
                    cpu_percents.append(cpu_percents2[i:i+2])
            elif len(cpu_percents2) % 3 == 0:
                cpu_percents = []
                for i in range(len(cpu_percents2) // 3):
                    cpu_percents.append(cpu_percents2[i:i+3])
            elif len(cpu_percents2) % 4 == 0:
                cpu_percents = []
                for i in range(len(cpu_percents2) // 4):
                    cpu_percents.append(cpu_percents2[i:i+4])
            elif len(cpu_percents2) % 7 == 0:
                cpu_percents = []
                for i in range(len(cpu_percents2) // 7):
                    cpu_percents.append(cpu_percents2[i:i+7])
    return cpu_percents

print(read_top_output())

def get_mem_progress_bar(c):
    return 100 - c[0] / (float(c[2]))

def get_mem_info(c):
    return "total: " + str(c[0]) + ", free: " + str(c[1]) + ", used: " + str(c[2])
app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        # return '''
        #        <form action='login' method='POST'>
        #         <input type='text' name='email' id='email' placeholder='email'/>
        #         <input type='password' name='password' id='password' placeholder='password'/>
        #         <input type='submit' name='submit'/>
        #        </form>
        #        '''
    
    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        #user = User()
        #user.id = email
        #flask_login.login_user(user)
        res = flask.make_response(flask.redirect("/index"))
        res.set_cookie('jwt', jwt.encode({"email": email}, "secret", algorithm="HS256"))
        return res

    return 'Bad login'

@app.route("/")
def hello_world():
    return flask.redirect('/index')

@app.route("/table_css")
def ret_table_css():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        top_parse = parse_top(read_top_output())
        return render_template('table_css.html', prs=top_parse[5])
    return flask.redirect('/login')

@app.route('/index/')
def index():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        top_parse = parse_top(read_top_output())
        return render_template('index.html', prs=top_parse[5], percent_mem=get_mem_progress_bar(parse_top(read_top_output())[3]), mem_info=get_mem_info(parse_top(read_top_output())[3]), cpu=cpu_usage())
    return flask.redirect('/login')

@app.route("/mem_info")
def mem_info():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        return render_template('mem_info.html', mem_info=get_mem_info(parse_top(read_top_output())[3]))
    return flask.redirect('/login')

@app.route("/mem_info_bar")
def mem_info_bar():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        return render_template('mem_info_bar.html', percent_mem=get_mem_progress_bar(parse_top(read_top_output())[3]))
    return flask.redirect('/login')

@app.route("/res_table")
def res():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        return render_template('table_result.html', prs=parse_htop(read_htop_output()))
    return flask.redirect('/login')

@app.route("/kill/<pid>")
def kill_pr(pid):
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        return str(kill_process(pid))+'<meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/index/" />'
    return flask.redirect('/login')

@app.route("/cpu_info")
def cpu_info():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        cpu_data = cpu_usage()
        return render_template('cpu_info.html', cpu=cpu_data)
    return flask.redirect('/login')

@app.route("/cpu_cores_count")
def cpu_cores_count():
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        cpu_info_abc = len(cpu_usage()) > 24
        if (len(cpu_usage()) > 24):
            return "0"
        else:
            return f"{len(cpu_info_abc)}"
    return flask.redirect('/login')

@app.route("/cpu_info_core/<core_numb>")
def cpu_info_core(core_numb):
    if flask.request.cookies.get("jwt") != '':
        try:
            t = jwt.decode(flask.request.cookies.get("jwt"), key='secret', algorithms="HS256")
        except:
            return flask.redirect('/login')
        # нумирация начинается с 0
        return cpu_usage()[core_numb]
    return flask.redirect('/login')
    
@app.route('/logout')
def logout():
    res = flask.make_response(flask.redirect('/login'))
    res.set_cookie('jwt', '')
    return res