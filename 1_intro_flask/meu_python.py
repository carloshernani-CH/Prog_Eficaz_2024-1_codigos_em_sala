from flask import Flask, request
import psycopg2 

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="zevkaiok",
    user="zevkaiok",
    password="j2F-SsTiodSnXBpyyQSoCAdoH_cKv9Ao",
    host="silly.db.elephantsql.com")

lista_alunos = []

@app.route("/")
def hello_world():
    return "<p>Web service em execução</p>"

@app.route("/cadastra_aluno", methods=["POST"])
def cadastra_aluno_func():
    dic_aluno = request.json
    nome = dic_aluno.get("nome", "")
    idade = dic_aluno.get("idade", 0)
    cpf = dic_aluno.get("cpf", None)
    email = dic_aluno.get("email", None)

    # DE OBRIGATORIO SERÃO OS CAMPOS CPF E EMAIL
    if not cpf or not email:
        return {"erro": "CPF e Email são obrigatórios"}, 400
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO alunos (nome, idade, cpf, email) VALUES (%s, %s, %s, %s)", (nome, idade, cpf, email))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    # resp de sucesso
    resp = {
        "mensagem": "Aluno cadastrado",
        "aluno": dic_aluno
    }
    return resp, 201


@app.route("/lista_alunos", methods=["GET"])
def lista_alunos_func():
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM alunos")
        lista_alunos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    alunos_lista = []
    for aluno in lista_alunos:
        alunos_lista.append({
            "id": aluno[0],
            "nome": aluno[1],
            "idade": aluno[4],
            "cpf": aluno[2],
            "email": aluno[3]
        })
    return alunos_lista, 200

if __name__ == "__main__":
    app.run(debug=True)
