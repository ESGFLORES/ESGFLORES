from flask import render_template, request, session, url_for
from datetime import date

from conexionBD import *  #Importando conexion BD
from funciones import *  #Importando mis Funciones
from routes import * #Vistas

import re
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template("index.html")  

@app.route('/login')
def login():
    return render_template("auth/login.html")

@ app.route('/ayuda')
def  ayuda():
    return render_template( 'ayuda.html' )


@app.route('/login', methods=['GET', 'POST'])
def loger():
    conexion_MySQLdb = connectionBD()
    if 'conectado' in session:
        return render_template('lector_ia.html', dataLogin = dataLoginSesion())
    else:
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email      = str(request.form['email'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE email = %s", [email])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'],password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas 
                    session['conectado']        = True
                    session['id']               = account['id']
                    session['tipo_user']        = account['tipo_user']
                    session['nombre']           = account['nombre']
                    session['apellido']         = account['apellido']
                    session['email']            = account['email']
                    session['sexo']             = account['sexo']
                    session['pais']             = account['pais']
                    session['create_at']        = account['create_at']
                    

                    msg = "Ha iniciado sesión correctamente."
                    return render_template('lector_ia.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion())                    
                else:
                    msg = 'Datos incorrectos, por favor revise si sus datos son correctos'
                    return render_template('index2.html', msjAlert = msg, typeAlert=0)
            else:
                return render_template('index2.html', msjAlert = msg, typeAlert=0)
    return render_template('index2.html', msjAlert = 'Debes iniciar sesión.', typeAlert=0)



#Registrando una cuenta de Usuario
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    msg = ''
    conexion_MySQLdb = connectionBD()
    if request.method == 'POST':
        tipo_user                   =2
        nombre                      = request.form['nombre']
        apellido                    = request.form['apellido']
        email                       = request.form['email']
        password                    = request.form['password']
        repite_password             = request.form['repite_password']
        sexo                        = request.form['sexo']
        
        pais                        = request.form['pais']
        create_at                   = date.today()
        #current_time = datetime.datetime.now()

        # Comprobando si ya existe la cuenta de Usuario con respecto al email
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        cursor.close() #cerrrando conexion SQL
          
        if account:
            msg = 'Ya existe el correo'
        elif password != repite_password:
            msg = 'Disculpa, las contraseñas no coinciden'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Formato de correo incorrecto'
        elif not email or not password or not password or not repite_password:
            msg = 'Has dejado campos vacíos en el formulario'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(password, method='sha256')
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute('INSERT INTO user (tipo_user, nombre, apellido, email, password, sexo, pais, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, email, password_encriptada, sexo, pais, create_at))
            conexion_MySQLdb.commit()
            cursor.close()
            msg = 'Su cuenta se creó correctamente'

        return render_template('index2.html', msjAlert = msg, typeAlert=1)
    return render_template('layout.html', dataLogin = dataLoginSesion(), msjAlert = msg, typeAlert=0)


if __name__ == '__main__':
   app.run(debug=True, port=3008)
