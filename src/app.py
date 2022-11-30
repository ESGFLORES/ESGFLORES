from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user

from config import config

from models.ModelUser import ModelUser

from models.entities.User import User

app = Flask(__name__)

db = MySQL(app)

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return render_template('lector_ia.html')
            else:
                flash("Contraseña inválida...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
 
@app.route('/lector_ia')
def lector():
    return render_template('lector_ia.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/agregando', methods = ['POST'])
def agregando():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO user(username, password, fullname) VALUES (%s, %s, %s)', 
        {username, password, fullname})
        db.connection.commit()
        return render_template('lector_ia.html')

@app.route('/agregar')
def agregar():
    return render_template('agregar.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=3008)