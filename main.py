from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb
import json
#https://www.it-swarm-es.com/es/python/usando-mysql-en-flask/941923326/
# Para ejecutar el servicio debo ejecutar main.py

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Iloveforyou'
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

@app.route('/logout')
def logout():
 if 'correo' in session:
  session.pop('correo', None)
 return redirect(url_for('sign_in'))

@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/info',methods=["GET","POST"])
def info():
    return render_template('info.html')

@app.route('/uso',methods=["GET","POST"])
def uso():
    return render_template('uso.html')

@app.route('/signUp', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        _email = request.form['correo']
        _password = request.form['contra']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuario (correo, password_) VALUES (%s,%s)", (_email, _password))
        #cursor.callproc('crearUsuario',(_email,_password))
        mysql.connection.commit()
        flash('Nuevo contacto agregado')
        return render_template('index.html')
    cursor.close()

@app.route('/validateLogin', methods = ['POST'])
def validateLogin():
    _email = request.form['correo']
    _password = request.form['contra']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE correo = %s AND password_ = %s", (_email, _password))  
    data = cursor.fetchall()
    if len(data) > 0:
        session['user'] = _email
        return redirect(url_for('transcripcion'))

    return render_template('index.html', error = 'Usuario no existe')
    cursor.close()

@app.route('/transcripcion',methods = ['POST','GET'])
def transcripcion():
    return render_template('transcripcion.html')


if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el main.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor