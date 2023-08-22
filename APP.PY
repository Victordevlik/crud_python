from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="productos"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    db.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        return render_template('editar.html', producto=producto)
    else:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        cursor.execute("UPDATE productos SET nombre = %s, precio = %s WHERE id = %s", (nombre, precio, id))
        db.commit()
        return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

