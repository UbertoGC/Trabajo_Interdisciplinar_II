from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb

#https://www.it-swarm-es.com/es/python/usando-mysql-en-flask/941923326/
# Para ejecutar el servicio debo ejecutar main.py

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<contraseña>'
app.config['MYSQL_DB'] = 'Almacen'
mysql = MySQL(app)

app.secret_key='mysecretkey'


@app.route('/')
def home():
    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('home.html')

@app.route('/sign_in',methods=["GET","POST"])
def sign_in():
    return render_template('index.html')

@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/info',methods=["GET","POST"])
def info():
    return render_template('info.html')


@app.route('/signUp', methods = ['POST','GET'])
def signUp():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if  _email and _password:
        conn = mysql.connect()
        if (conn):
            print("Conexion establecida")
        else:
            print("Conexion fallida")
        cursor = conn.cursor()
        cursor.callproc('crearUsuario',(_email, _password))
        data = cursor.fetchall()
        if len(data) ==0:
            conn.commit()
            print("Usuario fue creado!")
            return json.dumps({'mensaje':'usuario fue creado!'})
        else:
            print({'error':str(data[0])})
    else:
        return json.dumps({'mensaje': 'Campos estan vacios!'})
    cursor.close()
    conn.close()


if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el main.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor
