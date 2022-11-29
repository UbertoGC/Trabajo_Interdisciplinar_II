import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysql_connector import MySQL
from sonido import *

#https://www.it-swarm-es.com/es/python/usando-mysql-en-flask/941923326/
# Para ejecutar el servicio debo ejecutar main.py

app = Flask(__name__)
app.debug = True
app.secret_key ='secreto'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hardware+10'
app.config['MYSQL_DB'] = 'Almacen'
mysql = MySQL(app)
mysql.init_app(app)
valor=["Presiona el boton de play para iniciar",0]
app.secret_key='mysecretkey'
dic_cantidad={'un':'1','una':'1','dos':'2','tres':'3','cuatro':'4','cinco':'5','seis':'6','siete':'7','ocho':'8','nueve':'9','cero':'0'}
dic_u_medidas=['cucharada','pastilla']
dic_tiempo=['hora','día','semana','meses','mes']
valor = []
@app.route('/transcripcion',methods = ['POST','GET'])
def transcripcion():
    if(loop.is_running() and (not estado[0])):
        while(loop.is_running()):
            resultados=[]
        resultados=[]
        for i in guardado:
            menor=i.lower()
            diack=menor[:-1]
            resultados.append(diack.split())
        print(resultados)
        for j in resultados:
            lista=["-","-","-","Indefinida"]
            pri=True
            i = 0
            while(i<len(j)):
                if(pri):
                    while(i < len(j)):
                        if(j[i] in dic_cantidad):
                            if(lista[0] == "-"):
                                lista[0] = ""
                            lista[0] = lista[0]+dic_cantidad[j[i]]
                        else:
                            break
                        i+=1
                    if(i < len(j) and lista[0] != "-"):
                        if (j[i] in dic_u_medidas or (j[i])[:-1] in dic_u_medidas ):
                            lista[0] = lista[0] + " " + j[i]
                        else:
                            lista[0] = "-"
                    pri = False
                    i-=1
                elif(j[i] == "de"):
                    k = i + 1
                    while(k<len(j) and k>0):
                        if(j[k] != "cada" and j[k] != "por"):
                            if(lista[1] == "-"):
                                lista[1] = ""
                            lista[1] = lista[1] + " " + j[k]
                        else:
                            break
                        k += 1
                    i = (k - 1)
                elif(j[i] == "cada" or j[i] == "por"):
                    k=i+1
                    arc1="-"
                    arc2="-"
                    while(k<len(j)):
                        if(j[k] in dic_cantidad):
                            if(arc1=="-"):
                                arc1=""
                            arc1=arc1+dic_cantidad[j[k]]
                        else:
                            break
                        k+=1
                    det = 2
                    if(j[i] == "por"):
                        det = 3
                    print(det)
                    if(k<len(j)):
                        if(j[k] in dic_tiempo or (j[k])[:-1] in dic_tiempo):
                            arc2 = j[k]
                            if(arc1!="-"):
                                lista[det]= j[i] + " " + arc1 + " " + arc2
                            else:
                                lista[det]= j[i] + " " + arc2
                        else:
                            lista[det]= "-"
                    i=k
                i+=1
            valor.append(lista)
    elif(estado[0] and (not loop.is_running())):
        guardado.clear()
        loop.run_until_complete(Recibir_Enviar())
    return render_template('transcripcion.html', texto=guardado,valores=valor)

@app.route('/transenviplay')
def transenviplay():
    estado[0]=True
    return redirect(url_for('transcripcion'))

@app.route('/transenvistop')
def transenvistop():
    estado[0]=False
    return redirect(url_for('transcripcion'))

@app.route('/borrar')
def borrar():
    valor.clear()
    return redirect(url_for('transcripcion'))

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
        return render_template('index.html')
@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/info',methods=["GET","POST"])
def info():
    return render_template('info.html')

@app.route('/uso',methods=["GET","POST"])
def uso():
    return render_template('uso.html')
    
@app.route('/verPDF',methods=["GET","POST"])
def verPDF():
    return render_template('verPDF.html')

@app.route('/signUp', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        _email = request.form['correo']
        _password = request.form['contra']
        cursor = mysql.connection.cursor()
        cursor.execute("Use Almacen")
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
    cursor.execute("Use Almacen")
    cursor.execute("SELECT * FROM usuario WHERE correo = %s AND password_ = %s", (_email, _password))
    data = cursor.fetchall()
    if len(data) > 0:
        session['user'] = _email
        return redirect(url_for('transcripcion'))
    cursor.close()
    flash('Contraseña o usuario incorrecto')
    return redirect('sign_in')

if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el main.py entonces arranca el servidor
    app.run(port=5000,debug=True)#corre el servidor