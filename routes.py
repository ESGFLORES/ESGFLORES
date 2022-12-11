from flask import Flask, render_template, session
from funciones import *  #Importando mis Funciones


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'

    
    
#Creando mi Decorador para el Home
@app.route('/log')
def inicio():
    if 'conectado' in session:
        return render_template('index.html', dataLogin = dataLoginSesion())
    else:
        return render_template('index2.html')
    
    
@app.route('/login')
def logi():
    if 'conectado' in session:
        return render_template('index.html', dataLogin = dataLoginSesion())
    else:
        return render_template('index2.html')

   
# Cerrar session del usuario
@app.route('/logout')
def logout():
    msgClose = ''
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('email', None)
    msgClose ="La sesión fue cerrada correctamente"
    return render_template('index2.html', msjAlert = msgClose, typeAlert=1)

    