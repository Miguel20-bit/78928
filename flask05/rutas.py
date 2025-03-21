from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import Response
from modelos import Producto
import sqlite3

app = Flask(__name__)

productos = []

@app.route('/')
def inicio():
   con = conexion()
   productos = con.execute('SELECT * FROM productos').fetchall()
   con.close()
   return render_template('productos.html', productos=productos)

@app.route('/editar/<id>')
def editar(id):
    con = conexion()
    p = con.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    con.close()
    return render_template('editar.html', producto=p)

@app.route('/guardar', methods=['POST'])
def guardar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    id = request.form.get('id')
    print(f"{n} {p}  {id}")
    
    # i = 0
    # for e in productos:
    #     if e.nombre == n:
    #         productos[i] = Producto(n, p)
    #         print('Producto actualizado')
    #     i += 1

    con = conexion()
    con.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?', (n, p, id))
    con.commit()
    con.close()
    return Response("guardado" , headers={'Location': '/'}, status=302)

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    con = conexion()
    con.execute('DELETE FROM productos WHERE id = ?', (id,))
    con.commit()
    con.close()
    return redirect(url_for('inicio'))

@app.route('/crear', methods=['POST'])
def crear():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    con = conexion()
    con.execute('INSERT INTO productos (nombre, precio) VALUES (?, ?)', (n, p))
    con.commit()
    con.close()
    return redirect(url_for('inicio'))

def conexion():
    con = sqlite3.connect('basedatos.db')
    con.row_factory = sqlite3.Row
    return con

def iniciar_db():
    con = conexion()  
    
    con.execute('''
    CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
                )
    ''')
    con.commit()
    con.close()

if __name__ == '__main__':
    iniciar_db()
    app.run(host='0.0.0.0', debug=True)
