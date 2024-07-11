from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'User.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def home():
    return "Bienvenido al sistema de gestión de claves!"

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.json
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')
    print(f"Registrando usuario: {nombre}, {contrasena}")
    if not nombre or not contrasena:
        return jsonify({'error': 'Faltan parámetros'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, contrasena) VALUES (?, ?)', (nombre, contrasena))
    conn.commit()
    conn.close()
    print("Usuario registrado exitosamente")
    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.json
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')
    print(f"Intento de inicio de sesión para: {nombre}")
    if not nombre or not contrasena:
        return jsonify({'error': 'Faltan parámetros'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contrasena = ?', (nombre, contrasena))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Inicio de sesión exitoso")
        return jsonify({'mensaje': 'Inicio de sesión exitoso'})
    else:
        print("Credenciales inválidas")
        return jsonify({'error': 'Credenciales inválidas'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)

