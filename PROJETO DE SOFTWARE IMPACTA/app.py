from flask import Flask, render_template, request, redirect
import mysql.connector

# Cria a conexão com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    database="bd_agenda",
    user='root',
    password='Foreveralone@123'
)
cursor = conexao.cursor()

app = Flask(__name__)
app.secret_key = 'Foreveralone@123'

@app.route('/')
def index():
    return render_template('index.html')

#Testa a conexão com o banco de dados
@app.route('/teste')
def teste_conexao():
    if conexao.is_connected():
        cursor = conexao.cursor()
        return render_template('teste_conexao.html')
    conexao.close()
    cursor.close()

#Cadastra o formulário no banco de dados
@app.route('/cadastrar', methods=["POST","GET"])
def cadastrar():
    nome = request.form['form_nome']
    telefone = request.form['form_telefone']
    email = request.form['form_email']

    cursor.execute("INSERT INTO contatos (nome, telefone, email) VALUES(%s, %s, %s)",(nome, telefone, email))
    conexao.commit()

    return redirect('/') 
    
if __name__ == '__main__':
    app.run(debug=True)
