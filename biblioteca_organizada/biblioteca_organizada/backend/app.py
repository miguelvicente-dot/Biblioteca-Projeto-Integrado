from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from functools import wraps
from config import SECRET_KEY
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
from dao import LeitorDAO, LivroDAO, ReservaDAO, EmprestimoDAO, ContatoDAO, UsuarioDAO

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

def resposta_erro(mensagem, status=400):
    return jsonify({"erro": mensagem}), status

def login_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id_leitor" not in session:
            return resposta_erro("Faça login para continuar.", 401)
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def inicio():
    return send_from_directory(str(FRONTEND_DIR), "index.html")

@app.get("/api/status")
def status():
    return jsonify({"sistema": "Biblioteca", "online": True})

@app.get("/api/livros")
def listar_livros():
    busca = request.args.get("busca", "")
    return jsonify(LivroDAO.listar(busca))

@app.get("/api/livros/<int:id_livro>")
def buscar_livro(id_livro):
    livro = LivroDAO.buscar(id_livro)
    if not livro:
        return resposta_erro("Livro não encontrado.", 404)
    return jsonify(livro)

@app.post("/api/livros")
def cadastrar_livro():
    dados = request.get_json(silent=True) or {}
    obrigatorios = ["titulo", "isbn"]
    if any(not str(dados.get(campo, "")).strip() for campo in obrigatorios):
        return resposta_erro("Título e ISBN são obrigatórios.")
    try:
        novo_id = LivroDAO.criar(dados)
        return jsonify({"mensagem": "Livro cadastrado!", "id_livro": novo_id}), 201
    except Exception as erro:
        return resposta_erro("Não foi possível cadastrar. Verifique se o ISBN já existe.", 409)

@app.put("/api/livros/<int:id_livro>")
def atualizar_livro(id_livro):
    dados = request.get_json(silent=True) or {}
    if not dados.get("titulo") or not dados.get("isbn"):
        return resposta_erro("Título e ISBN são obrigatórios.")
    if not LivroDAO.buscar(id_livro):
        return resposta_erro("Livro não encontrado.", 404)
    try:
        LivroDAO.atualizar(id_livro, dados)
        return jsonify({"mensagem": "Livro atualizado!"})
    except Exception:
        return resposta_erro("Não foi possível atualizar. Confira o ISBN.", 409)

@app.delete("/api/livros/<int:id_livro>")
def excluir_livro(id_livro):
    if not LivroDAO.buscar(id_livro):
        return resposta_erro("Livro não encontrado.", 404)
    try:
        LivroDAO.excluir(id_livro)
        return jsonify({"mensagem": "Livro excluído!"})
    except Exception:
        return resposta_erro("Este livro possui registros vinculados e não pode ser excluído.", 409)

@app.get("/api/autores")
def listar_autores():
    return jsonify(LivroDAO.listar_autores())

@app.post("/api/autores")
def cadastrar_autor():
    dados = request.get_json(silent=True) or {}
    if not str(dados.get("nome", "")).strip():
        return resposta_erro("O nome do autor é obrigatório.")
    novo_id = LivroDAO.criar_autor(dados)
    return jsonify({"mensagem": "Autor cadastrado!", "id_autor": novo_id}), 201

@app.post("/api/cadastro")
def cadastro():
    dados = request.get_json(silent=True) or {}
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip().lower()
    senha = str(dados.get("senha", ""))
    telefone = str(dados.get("telefone", "")).strip()
    if not nome or "@" not in email or len(senha) < 6:
        return resposta_erro("Informe nome, e-mail válido e senha com pelo menos 6 caracteres.")
    try:
        id_leitor = LeitorDAO.criar(nome, email, telefone)
        UsuarioDAO.criar(id_leitor, email, senha)
        return jsonify({"mensagem": "Cadastro realizado! Agora você pode entrar."}), 201
    except Exception:
        return resposta_erro("Este e-mail já está cadastrado.", 409)

@app.post("/api/login")
def login():
    dados = request.get_json(silent=True) or {}
    usuario = UsuarioDAO.autenticar(str(dados.get("email", "")).strip().lower(), str(dados.get("senha", "")))
    if not usuario:
        return resposta_erro("E-mail ou senha incorretos.", 401)
    session.clear()
    session["id_leitor"] = usuario["id_leitor"]
    session["nome"] = usuario["nome"]
    session["email"] = usuario["email"]
    return jsonify({"mensagem": "Login realizado!", "usuario": usuario})

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"mensagem": "Você saiu da sua conta."})

@app.get("/api/sessao")
def sessao():
    if "id_leitor" not in session:
        return jsonify({"logado": False})
    return jsonify({"logado": True, "usuario": {
        "id_leitor": session["id_leitor"], "nome": session["nome"], "email": session["email"]
    }})

@app.post("/api/reservas")
@login_obrigatorio
def reservar():
    dados = request.get_json(silent=True) or {}
    id_livro = dados.get("id_livro")
    if not id_livro or not LivroDAO.buscar(int(id_livro)):
        return resposta_erro("Livro não encontrado.")
    if ReservaDAO.tem_ativa(session["id_leitor"], int(id_livro)):
        return resposta_erro("Você já tem uma reserva ativa deste livro.")
    ReservaDAO.criar(session["id_leitor"], int(id_livro))
    return jsonify({"mensagem": "Reserva solicitada com sucesso!"}), 201

@app.get("/api/reservas")
@login_obrigatorio
def minhas_reservas():
    return jsonify(ReservaDAO.listar_do_leitor(session["id_leitor"]))

@app.get("/api/emprestimos")
@login_obrigatorio
def meus_emprestimos():
    return jsonify(EmprestimoDAO.listar_do_leitor(session["id_leitor"]))

@app.post("/api/contato")
def contato():
    dados = request.get_json(silent=True) or {}
    campos = ["nome", "email", "assunto", "mensagem"]
    if any(not str(dados.get(campo, "")).strip() for campo in campos):
        return resposta_erro("Preencha todos os campos.")
    ContatoDAO.criar(dados)
    return jsonify({"mensagem": "Mensagem enviada com sucesso!"}), 201

@app.get("/api/contato")
def listar_contatos():
    # Para um projeto escolar, esta rota permite conferir as mensagens salvas.
    return jsonify(ContatoDAO.listar())

if __name__ == "__main__":
    app.run(debug=True)
