import sqlite3
from flask import Flask, render_template, request, redirect, session, g
import os

app = Flask(__name__)
app.secret_key = 'segredo-superseguro'

DATABASE = 'agenda.db'

# ==============================
# BANCO: Conexão + criação
# ==============================

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            observacoes TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()

# ==============================
# ROTAS
# ==============================

@app.before_request
def garantir_banco():
    if not os.path.exists(DATABASE):
        criar_tabelas()

@app.route('/')
def index():
    if 'email' in session:
        return redirect('/agenda')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '').strip()

    if not email or not senha:
        return render_template('index.html', erro='Preencha todos os campos.', mostrar_login=True)

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cur.fetchone()
    conn.close()

    if usuario:
        session['email'] = usuario['email']
        session['nome'] = usuario['nome']
        session['usuario_id'] = usuario['id']
        return redirect('/agenda')
    else:
        return render_template('index.html', erro='E-mail ou senha incorretos.', mostrar_login=True)

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')
    confirmar = request.form.get('confirmar', '')

    if not nome or not email or not senha or not confirmar:
        return render_template('index.html', erro='Preencha todos os campos.', mostrar_login=False)
    if len(nome) < 4:
        return render_template('index.html', erro='O nome precisa ter pelo menos 4 caracteres.', mostrar_login=False)
    if senha != confirmar:
        return render_template('index.html', erro='As senhas não coincidem.', mostrar_login=False)

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return render_template('index.html', erro='E-mail já cadastrado.', mostrar_login=False)

    cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
    conn.commit()
    usuario_id = cur.lastrowid
    conn.close()

    session['email'] = email
    session['nome'] = nome
    session['usuario_id'] = usuario_id
    return redirect('/agenda')

@app.route('/agenda')
def agenda():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario_id = session['usuario_id']
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contatos WHERE usuario_id = ?", (usuario_id,))
    contatos = cur.fetchall()
    conn.close()

    return render_template('agenda.html', contatos=contatos, nome=session['nome'])

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario_id = session['usuario_id']
    contato_id = request.form.get('id')
    nome = request.form.get('nome', '').strip()
    telefone = request.form.get('telefone', '').strip()
    email_c = request.form.get('email', '').strip()
    obs = request.form.get('observacoes', '').strip()

    if not nome or not telefone or not email_c:
        return redirect('/agenda')  # opcional: exibir erro

    conn = conectar()
    cur = conn.cursor()

    if contato_id:
        cur.execute("""
            UPDATE contatos
            SET nome = ?, telefone = ?, email = ?, observacoes = ?
            WHERE id = ? AND usuario_id = ?
        """, (nome, telefone, email_c, obs, contato_id, usuario_id))
    else:
        cur.execute("""
            INSERT INTO contatos (usuario_id, nome, telefone, email, observacoes)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario_id, nome, telefone, email_c, obs))

    conn.commit()
    conn.close()
    return redirect('/agenda')

@app.route('/remover', methods=['POST'])
def remover():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario_id = session['usuario_id']
    contato_id = request.form.get('id')

    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM contatos WHERE id = ? AND usuario_id = ?", (contato_id, usuario_id))
    conn.commit()
    conn.close()

    return redirect('/agenda')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ==============================
# EXECUÇÃO
# ==============================

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)
