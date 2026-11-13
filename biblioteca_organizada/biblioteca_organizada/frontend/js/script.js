const API = "/api";

async function requisicao(url, opcoes = {}) {
  const resposta = await fetch(API + url, {
    credentials: "same-origin",
    headers: {"Content-Type": "application/json"},
    ...opcoes
  });
  const dados = await resposta.json();
  if (!resposta.ok) throw new Error(dados.erro || "Ocorreu um erro.");
  return dados;
}

function avisar(texto) {
  const caixa = document.getElementById("aviso");
  caixa.textContent = texto;
  caixa.classList.add("mostrar");
  setTimeout(() => caixa.classList.remove("mostrar"), 3500);
}

function abrirPagina(tipo) {
  const conteudo = document.getElementById("conteudoModal");
  if (tipo === "login") {
    conteudo.innerHTML = `<h2>Entrar na conta</h2>
      <form id="formLogin"><label>E-mail<input name="email" type="email" required></label>
      <label>Senha<input name="senha" type="password" required></label>
      <button class="btn">Entrar</button></form>
      <p class="alternar" onclick="abrirPagina('cadastro')">Ainda não tem conta? Cadastre-se.</p>`;
    document.getElementById("formLogin").addEventListener("submit", fazerLogin);
  } else {
    conteudo.innerHTML = `<h2>Criar cadastro</h2>
      <form id="formCadastro"><label>Nome<input name="nome" required></label>
      <label>E-mail<input name="email" type="email" required></label>
      <label>Telefone<input name="telefone"></label>
      <label>Senha (mínimo 6 caracteres)<input name="senha" type="password" minlength="6" required></label>
      <button class="btn">Cadastrar</button></form>
      <p class="alternar" onclick="abrirPagina('login')">Já tem conta? Entrar.</p>`;
    document.getElementById("formCadastro").addEventListener("submit", fazerCadastro);
  }
  document.getElementById("modal").classList.remove("escondido");
}
function fecharModal() { document.getElementById("modal").classList.add("escondido"); }

async function fazerLogin(evento) {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(evento.target));
  try {
    const retorno = await requisicao("/login", {method:"POST",body:JSON.stringify(dados)});
    fecharModal(); avisar(retorno.mensagem); await atualizarConta();
  } catch (erro) { avisar(erro.message); }
}
async function fazerCadastro(evento) {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(evento.target));
  try {
    const retorno = await requisicao("/cadastro", {method:"POST",body:JSON.stringify(dados)});
    avisar(retorno.mensagem); abrirPagina("login");
  } catch (erro) { avisar(erro.message); }
}
async function sair() {
  await requisicao("/logout", {method:"POST",body:"{}"});
  avisar("Você saiu da conta."); atualizarConta();
}
async function atualizarConta() {
  const dados = await requisicao("/sessao");
  const area = document.getElementById("areaUsuario");
  if (dados.logado) {
    area.innerHTML = `<span>Olá, ${escapar(dados.usuario.nome)}</span> <button class="btn btn-claro" onclick="sair()">Sair</button>`;
    carregarReservas(); carregarEmprestimos();
  } else {
    area.innerHTML = `<button class="btn btn-claro" onclick="abrirPagina('login')">Entrar</button>`;
    document.getElementById("listaReservas").textContent = "Entre na sua conta para consultar suas reservas.";
    document.getElementById("listaEmprestimos").textContent = "Entre na sua conta para consultar seus empréstimos.";
  }
}
function escapar(texto) {
  return String(texto ?? "").replace(/[&<>"']/g, caractere => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[caractere]));
}
async function carregarLivros() {
  const busca = document.getElementById("campoBusca").value;
  const livros = await requisicao("/livros?busca=" + encodeURIComponent(busca));
  const lista = document.getElementById("listaLivros");
  if (!livros.length) { lista.innerHTML = "<p>Nenhum livro encontrado.</p>"; return; }
  lista.innerHTML = livros.map(livro => `<article class="livro"><div class="capa">📘</div><div>
    <h3>${escapar(livro.titulo)}</h3><p>${escapar(livro.autores || "Autor não informado")}</p>
    <small>${escapar(livro.ano_publicacao || "Ano não informado")} · ISBN ${escapar(livro.isbn)}</small><br>
    <button class="btn" onclick="reservar(${livro.id_livro})">Reservar livro</button>
    </div></article>`).join("");
}
async function reservar(id) {
  try {
    const retorno = await requisicao("/reservas", {method:"POST",body:JSON.stringify({id_livro:id})});
    avisar(retorno.mensagem); carregarReservas();
  } catch (erro) { avisar(erro.message); }
}
async function carregarReservas() {
  try {
    const reservas = await requisicao("/reservas");
    const area = document.getElementById("listaReservas");
    if (!reservas.length) { area.textContent = "Você ainda não fez reservas."; return; }
    area.innerHTML = `<table class="tabela"><tr><th>Livro</th><th>Data</th><th>Status</th></tr>${reservas.map(r=>`<tr><td>${escapar(r.titulo)}</td><td>${dataBR(r.data_reserva)}</td><td><span class="status">${escapar(r.status)}</span></td></tr>`).join("")}</table>`;
  } catch (erro) { document.getElementById("listaReservas").textContent = erro.message; }
}
async function carregarEmprestimos() {
  try {
    const itens = await requisicao("/emprestimos");
    const area = document.getElementById("listaEmprestimos");
    if (!itens.length) { area.textContent = "Você ainda não possui empréstimos registrados."; return; }
    area.innerHTML = `<table class="tabela"><tr><th>Livro</th><th>Empréstimo</th><th>Prevista</th><th>Devolução</th></tr>${itens.map(e=>`<tr><td>${escapar(e.titulo)}</td><td>${dataBR(e.data_emprestimo)}</td><td>${dataBR(e.data_prevista)}</td><td>${e.data_devolucao ? dataBR(e.data_devolucao) : "Em aberto"}</td></tr>`).join("")}</table>`;
  } catch (erro) { document.getElementById("listaEmprestimos").textContent = erro.message; }
}
function dataBR(data) {
  if (!data) return "-";
  const parte = String(data).slice(0,10).split("-");
  return parte.length === 3 ? `${parte[2]}/${parte[1]}/${parte[0]}` : data;
}
document.getElementById("formContato").addEventListener("submit", async evento => {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(evento.target));
  try {
    const retorno = await requisicao("/contato", {method:"POST",body:JSON.stringify(dados)});
    avisar(retorno.mensagem); evento.target.reset();
  } catch (erro) { avisar(erro.message); }
});

carregarLivros();
atualizarConta();
