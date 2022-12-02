from flask import Flask,  render_template, request, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registro'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")  

@app.route('/login')
def login():
    return render_template("auth/login.html")

@ app.route('/ayuda')
def  ayuda():
    return render_template( 'ayuda.html' )

@app.route('/templates/agregar.html', methods = ["GET", "POST"])
def agregar():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user")
    tipo = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user")
    interes = cursor.fetchall()

    cursor.close()

    

    if request.method == 'GET':
        return render_template("agregar.html", tipo = tipo, interes = interes )
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']
        interes = request.form['interes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user (name, email, password, id_tip_usu, interes) VALUES (%s,%s,%s,%s,%s)", (name, email, password,tip,interes,))
        mysql.connection.commit()
        #notificacion.title = "Registro realizado con éxito"
        #notificacion.message="ya te encuentras registrado en 🤵 MORE LOVE 👰, por favor inicia sesión y empieza a descubrir este nuevo mundo."
        #notificacion.send()
        return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug=True, port=3008)
