from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Foreveralone@123'


# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        database="bd_agenda",
        user='root',
        password='Foreveralone@123'
    )


# Rota para a página de cadasto
@app.route('/')
def index():
    return render_template('index.html')


# Cadastra o formulário no banco de dados
@app.route('/cadastrar', methods=["POST", "GET"])
def cadastrar():
    nome = request.form['form_nome']
    telefone = request.form['form_telefone']
    email = request.form['form_email']

    conexao = conecta_banco()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO contatos (nome, telefone, email) VALUES(%s, %s, %s)",
        (nome, telefone, email))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect('/')


# Rota para a página de contatos
@app.route('/contatos')
def contatos():
    dados = exibir_dados()
    return render_template('contatos.html', dados=dados)


# Função para exibir contatos cadastrados
def exibir_dados():
    try:
        conexao = conecta_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, telefone, email FROM Contatos ORDER BY Nome ASC"
            )
        rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        rows = []
    finally:
        cursor.close()
        conexao.close()
    return rows


# Rota para apagar os contatos
@app.route('/deletar/<int:id>', methods=["POST", "GET"])
def deletar(id):
    try:
        conexao = conecta_banco()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = %s", (id,))
        conexao.commit()
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        cursor.close()
        conexao.close()
    return redirect('/contatos')


# Rota para edição de contatos
@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id: int):
    if request.method == "POST":
        nome = request.form['form_nome']
        telefone = request.form['form_telefone']
        email = request.form['form_email']

        conexao = conecta_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE contatos SET nome=%s, telefone=%s, email=%s WHERE id=%s", (
                nome, telefone, email, id
            )
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect('/contatos')
    else:
        conexao = conecta_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, telefone, email FROM contatos WHERE id=%s", (
                id,
            )
        )
        contato = cursor.fetchone()
        cursor.close()
        conexao.close()
        return render_template('editar.html', contato=contato, id=id)  


if __name__ == '__main__':
    app.run(debug=True)
