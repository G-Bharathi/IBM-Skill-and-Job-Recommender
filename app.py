from flask import Flask,render_template,request,session
from flask_session import Session
import ibm_db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;UID=xwl60917;PWD=07oTqMW5aEHHUiAK;",'','')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['POST'])
def login():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    sql = 'INSERT INTO jobregistration values(?,?,?)'
    prepare_stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(prepare_stmt,1,name)
    ibm_db.bind_param(prepare_stmt,2,email)
    ibm_db.bind_param(prepare_stmt,3,password)
    ibm_db.execute(prepare_stmt)
    return render_template('login.html',msg = 'Registration successful')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/welcome',methods=['POST'])
def welcome():
    email = request.form['email']
    password = request.form['password']
    sql = "select name from jobregistration where email=? AND password=?"
    prep_stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(prep_stmt, 1, email)
    ibm_db.bind_param(prep_stmt, 2, password)
    ibm_db.execute(prep_stmt)
    values = ibm_db.fetch_assoc(prep_stmt)
    if values:
        session['name'] = values['NAME']
        return render_template("home.html")
    else:
        session['error'] = "Incorrect email or password!"
        return render_template("login.html")

if __name__ == '__main__':  
    app.run(debug=True)