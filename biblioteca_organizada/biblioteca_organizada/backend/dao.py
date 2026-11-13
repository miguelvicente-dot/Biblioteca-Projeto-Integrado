from database import conectar
from werkzeug.security import generate_password_hash, check_password_hash

# DAO: classes responsáveis por conversar com o banco de dados.

class LeitorDAO:
    @staticmethod
    def criar(nome, email, telefone):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO leitor (nome,email,telefone) VALUES (%s,%s,%s)", (nome,email,telefone))
        conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conexao.close()
        return novo_id

class UsuarioDAO:
    @staticmethod
    def criar(id_leitor, email, senha):
        conexao = conectar()
        cursor = conexao.cursor()
        senha_hash = generate_password_hash(senha)
        cursor.execute("INSERT INTO usuario (id_leitor,email,senha_hash) VALUES (%s,%s,%s)", (id_leitor,email,senha_hash))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def autenticar(email, senha):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""SELECT u.id_leitor,u.email,u.senha_hash,l.nome
                          FROM usuario u JOIN leitor l ON l.id_leitor=u.id_leitor
                          WHERE u.email=%s""", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()
        if usuario and check_password_hash(usuario["senha_hash"], senha):
            usuario.pop("senha_hash")
            return usuario
        return None

class LivroDAO:
    @staticmethod
    def listar(busca=""):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        termo = f"%{busca}%"
        cursor.execute("""SELECT l.id_livro,l.titulo,l.isbn,l.ano_publicacao,
                          GROUP_CONCAT(a.nome SEPARATOR ', ') AS autores
                          FROM livro l
                          LEFT JOIN livro_autor la ON la.id_livro=l.id_livro
                          LEFT JOIN autor a ON a.id_autor=la.id_autor
                          WHERE l.titulo LIKE %s OR l.isbn LIKE %s OR a.nome LIKE %s
                          GROUP BY l.id_livro ORDER BY l.titulo""", (termo,termo,termo))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados

    @staticmethod
    def buscar(id_livro):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM livro WHERE id_livro=%s", (id_livro,))
        livro = cursor.fetchone()
        cursor.close()
        conexao.close()
        return livro

    @staticmethod
    def criar(dados):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO livro (titulo,isbn,ano_publicacao) VALUES (%s,%s,%s)",
                       (dados["titulo"],dados["isbn"],dados.get("ano_publicacao") or None))
        novo_id = cursor.lastrowid
        id_autor = dados.get("id_autor")
        if id_autor:
            cursor.execute("INSERT INTO livro_autor (id_livro,id_autor) VALUES (%s,%s)", (novo_id,id_autor))
        conexao.commit()
        cursor.close()
        conexao.close()
        return novo_id

    @staticmethod
    def atualizar(id_livro, dados):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE livro SET titulo=%s,isbn=%s,ano_publicacao=%s WHERE id_livro=%s",
                       (dados["titulo"],dados["isbn"],dados.get("ano_publicacao") or None,id_livro))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id_livro):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM livro_autor WHERE id_livro=%s", (id_livro,))
        cursor.execute("DELETE FROM livro WHERE id_livro=%s", (id_livro,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def listar_autores():
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM autor ORDER BY nome")
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados

    @staticmethod
    def criar_autor(dados):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO autor (nome,nacionalidade) VALUES (%s,%s)",
                       (dados["nome"],dados.get("nacionalidade","")))
        novo_id = cursor.lastrowid
        conexao.commit()
        cursor.close()
        conexao.close()
        return novo_id

class ReservaDAO:
    @staticmethod
    def tem_ativa(id_leitor, id_livro):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""SELECT COUNT(*) FROM reserva WHERE id_leitor=%s AND id_livro=%s
                          AND status IN ('Pendente','Aprovada')""", (id_leitor,id_livro))
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        conexao.close()
        return existe

    @staticmethod
    def criar(id_leitor, id_livro):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO reserva (id_leitor,id_livro,data_reserva,status) VALUES (%s,%s,CURDATE(),'Pendente')",
                       (id_leitor,id_livro))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def listar_do_leitor(id_leitor):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""SELECT r.id_reserva,r.data_reserva,r.status,l.titulo
                          FROM reserva r JOIN livro l ON l.id_livro=r.id_livro
                          WHERE r.id_leitor=%s ORDER BY r.id_reserva DESC""", (id_leitor,))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados

class EmprestimoDAO:
    @staticmethod
    def listar_do_leitor(id_leitor):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""SELECT e.id_emprestimo,e.data_emprestimo,e.data_prevista,e.data_devolucao,l.titulo
                          FROM emprestimo e JOIN livro l ON l.id_livro=e.id_livro
                          WHERE e.id_leitor=%s ORDER BY e.id_emprestimo DESC""", (id_leitor,))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados

class ContatoDAO:
    @staticmethod
    def criar(dados):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO contato (nome,email,assunto,mensagem,data_envio) VALUES (%s,%s,%s,%s,NOW())",
                       (dados["nome"],dados["email"],dados["assunto"],dados["mensagem"]))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def listar():
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_contato,nome,email,assunto,mensagem,data_envio FROM contato ORDER BY id_contato DESC")
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados
