from flask import Flask, render_template, request
from flask import redirect, url_for
from modelos import Producto

app = Flask(__name__)

productos = []

@app.route('/')
def inicio():
    global productos
    productos = [Producto("Impresora", 500), Producto("Computadora", 620), Producto("Mouse", 150)]
    return render_template('productos.html', productos=productos)

@app.route('/editar/<producto>/<precio>')
def editar(producto, precio):
    print(producto)
    print(precio)
    return render_template('editar.html', producto=producto, precio=precio)

@app.route('/guardar', methods=['POST'])
def guardar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    
    i = 0
    for e in productos:
        if e.nombre == n:
            productos[i] = Producto(n, p)
            print('Producto actualizado')
        i += 1
    return 'Producto guardado correctamente'

@app.route('/eliminar/<nombre>', methods=['GET'])
def eliminar(nombre):
    global productos
    for i, e in enumerate(productos):
        if e.nombre == nombre:
            print(f'Eliminando producto: {e.nombre}')
            productos.pop(i)
            break
    return 'Producto eliminado correctamente'

@app.route('/crear', methods=['POST'])
def crear():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    productos.append(Producto(n, p))
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
