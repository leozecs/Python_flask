# 📒 Agenda de Contatos (Flask)

Este é um projeto completo de **Agenda de Contatos** desenvolvido com **Python + Flask**. A aplicação permite que usuários se cadastrem, façam login e gerenciem seus próprios contatos de forma privada e segura.

## ✨ Funcionalidades

- ✅ Cadastro de usuário com nome, e-mail, senha e confirmação de senha
- ✅ Login e logout seguro (com autenticação por e-mail e senha)
- ✅ Separação de dados por usuário (cada um vê só seus contatos)
- ✅ Cadastro de contatos (nome, telefone, e-mail, observações)
- ✅ Edição e remoção de contatos
- ✅ Layout moderno e responsivo
- ✅ Tema claro/escuro com animações em JS
- ✅ Design com abas (login/cadastro e agenda) em tela única
- ✅ Banco de dados SQLite para armazenamento local

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/index.html)
- HTML5, CSS3 e JavaScript (JS puro)
- Bootstrap-like visual (manual)
- Jinja2 (template engine do Flask)

---

## 💾 Como Rodar o Projeto Localmente

### 1. Clone o repositório:

```bash
git clone https://github.com/leozecs/Python-flask.git
cd agenda-projeto-completo

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

3. Instale as dependências:
pip install flask

4. Execute o app:
python app.py

5. Acesse no navegador:
http://localhost:5000

📁 Estrutura de Arquivos

agenda-flask/
├── app.py
├── templates/
│   ├── index.html
│   └── agenda.html
├── static/
│   ├── styles.css
│   └── scripts.js
└── database/
    └── agenda.db

 🔐 Segurança
As senhas são armazenadas com hash.

Sessões são utilizadas para manter o usuário autenticado.

Proteção contra acesso não autorizado a rotas da agenda.

📌 Possíveis Melhorias Futuras
Integração com banco PostgreSQL ou MySQL

Deploy no Render, Vercel, ou Heroku

Upload de foto de perfil

Busca e filtro de contatos

API RESTful para mobile apps

👨‍💻 Autor
Leonardo Tavares
