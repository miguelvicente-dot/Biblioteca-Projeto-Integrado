# Sistema de Biblioteca — Projeto Integrado DWS + POO + BD

Projeto escolar organizado em pastas, utilizando Python, Flask, POO, DAO, MySQL, HTML, CSS e JavaScript.

## Estrutura do projeto

```text
biblioteca_organizada/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── dao.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── database/
│   └── banco.sql
│
├── docs/
│   └── diagrama_classes.mmd
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Para que serve cada pasta?

- `backend/`: Python, Flask, classes, conexão e operações DAO.
- `frontend/`: páginas e arquivos que o usuário vê no navegador.
- `frontend/css/`: aparência do site.
- `frontend/js/`: interações e chamadas Fetch para a API.
- `database/`: criação das tabelas e dados iniciais do MySQL.
- `docs/`: documentação e diagrama de classes.

## Instalação

### 1. Banco de dados
1. Abra o XAMPP e inicie o MySQL.
2. Acesse `http://localhost/phpmyadmin`.
3. Importe `database/banco.sql`.

### 2. Instalar bibliotecas Python
Abra o terminal na pasta principal do projeto e execute:

```bash
pip install -r requirements.txt
```

### 3. Executar
Ainda na pasta principal, execute:

```bash
python backend/app.py
```

Abra `http://127.0.0.1:5000`.

Não abra `index.html` diretamente nem use Live Server. O Flask serve o front-end e as rotas da API.

## Arquivos do back-end

- `app.py`: rotas Flask e validação das requisições.
- `config.py`: configurações do MySQL e chave de sessão.
- `database.py`: função que abre a conexão com MySQL.
- `models.py`: classes que representam as entidades.
- `dao.py`: comandos de consulta e alteração no banco.

## Como explicar

**DWS:** HTML, CSS e JavaScript formam a parte visual. O JavaScript usa `fetch()` para enviar e receber dados das rotas Flask.

**POO:** as classes `Leitor`, `Livro`, `Autor`, `Reserva`, `Emprestimo` e `Contato` representam objetos do sistema.

**DAO:** os DAOs separam o código que acessa o banco de dados das rotas do sistema.

**BD:** MySQL guarda leitores, livros, autores, empréstimos, usuários, reservas e mensagens.

**Flask:** recebe as requisições, chama os DAOs e retorna respostas em JSON.

## GitHub

Execute os comandos na pasta principal:

```bash
git init
git add .
git commit -m "Etapa 1 - Banco e estrutura do projeto"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

Faça novos commits durante o desenvolvimento. Adicione o professor como colaborador pelo menu Settings > Collaborators:
`leonardo.stephan@eaportal.org`

## Observações
- O sistema começa com livros de exemplo.
- O cadastro cria um leitor e um usuário. A senha é armazenada com hash.
- A reserva começa com status `Pendente`.
- A consulta de empréstimos mostra os registros lançados no banco.
- As rotas de CRUD de livros existem para demonstração; antes de publicar, devem receber controle de acesso administrativo.
