# Webservice - Não REST - com Flask e PostgreSQL

# doc: https://www.tutorialspoint.com/python_data_access/python_postgresql_introduction.htm

from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Configuração da conexão com o banco de dados
conn = psycopg2.connect(
    dbname="",
    user="",
    password="",
    host=""
)

@app.route("/")
def hello_world():
    return "<p>Web service em execução</p>"


@app.route('/cadastra_aluno', methods=['POST'])
def cadastra_aluno_func():
    dic_aluno = request.json
    nome = dic_aluno['nome']
    cpf = dic_aluno['cpf']
    email = dic_aluno['email']
    idade = dic_aluno['idade']

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO alunos (nome, cpf, email, idade) VALUES (%s, %s, %s, %s)",
                    (nome, cpf, email, idade))
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()  # Reverte a transação atual
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    # resp de sucesso
    resp = {
        "mensagem": "Aluno cadastrado",
        "aluno": dic_aluno
    }
    return resp, 201


@app.route('/lista_alunos', methods=['GET'])
def lista_alunos_func():
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM alunos")
        alunos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    alunos_lista = []
    for aluno in alunos:
        alunos_lista.append({
            "id": aluno[0],
            "nome": aluno[1],
            "cpf": aluno[2],
            "email": aluno[3],
            "idade": aluno[4]
        })

    return alunos_lista



if __name__ == "__main__":
    app.run(debug=True)
