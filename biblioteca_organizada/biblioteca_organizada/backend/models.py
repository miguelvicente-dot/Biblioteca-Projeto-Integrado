# Classes simples do sistema (POO).

class Leitor:
    def __init__(self, nome, email, telefone=""):
        self.nome = nome
        self.email = email
        self.telefone = telefone

class Livro:
    def __init__(self, titulo, isbn, ano_publicacao=None):
        self.titulo = titulo
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao

class Autor:
    def __init__(self, nome, nacionalidade=""):
        self.nome = nome
        self.nacionalidade = nacionalidade

class Reserva:
    def __init__(self, id_leitor, id_livro, status="Pendente"):
        self.id_leitor = id_leitor
        self.id_livro = id_livro
        self.status = status

class Emprestimo:
    def __init__(self, id_leitor, id_livro, data_emprestimo, data_prevista):
        self.id_leitor = id_leitor
        self.id_livro = id_livro
        self.data_emprestimo = data_emprestimo
        self.data_prevista = data_prevista

class Contato:
    def __init__(self, nome, email, assunto, mensagem):
        self.nome = nome
        self.email = email
        self.assunto = assunto
        self.mensagem = mensagem
