# Daze Login

Tela de login com front-end em HTML/CSS/JS e back-end em Python (Flask + SQLite).

## Sobre o projeto

Eu criei este projeto para estudar, como funciona um sistema de login completo, da tela que o usuário vê até o banco de dados que guarda as informações. Comecei com uma tela de login só em HTML e CSS e fui evoluindo aos poucos: primeiro melhorei o front-end com validação e acessibilidade, depois construí o back-end para que o login realmente funcionasse.

Meu objetivo não foi fazer um projeto grnade, e sim um básico, porém bem detalhado, que me fizesse passar por vários assuntos diferentes ao mesmo tempo: HTML, CSS, JavaScript, Python, banco de dados, segurança e Git.

## Tecnologias
- Flask, SQLite, Flask-Limiter, python-dotenv
- Hash de senha (Werkzeug), sessão com cookie seguro
- Rate limiting contra força bruta

## O que eu implementei

- Escolhi guardar as senhas apenas como hash, para que ninguém consiga ver a senha original, nem mesmo eu.
- Usei consultas SQL parametrizadas para me proteger de SQL Injection.
- Configurei a sessão com cookie seguro (`HttpOnly` e `SameSite`).
- Limitei as tentativas de login para dificultar ataques de força bruta.
- Deixei a mensagem de erro genérica ("Usuário ou senha inválidos"), para não revelar quais usuários existem.
- Guardei a chave secreta num arquivo `.env`, que nunca vai para o GitHub.

## Como rodar
1. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e gere uma chave:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
4. Crie um usuário:
   ```
   python criar_usuario.py
   ```
5. Suba o servidor:
   ```
   python app.py
   ```
6. Acesse http://127.0.0.1:5000

## Estrutura do projeto

```
pagina-login/
├── app.py                 # rotas e regras do servidor
├── database.py            # conexão e criação do banco
├── criar_usuario.py       # cria usuários pelo terminal
├── redefinir_senha.py     # troca a senha de um usuário
├── requirements.txt
├── .env.example           # modelo das variáveis de ambiente
├── templates/             # index.html e painel.html
└── static/                # styles.css, script.js e imagens
```

## O que eu aprendi

- Como o front-end e o back-end conversam, usando `fetch` e respostas em JSON.
- Por que senha nunca deve ser guardada em texto puro, e como funciona o hash.
- A diferença entre `.env` (segredo, fica só no meu computador) e `.env.example` (modelo público).
- Como usar o Git e o GitHub, incluindo o `.gitignore` para proteger arquivos sensíveis.
- A importância de olhar o Console do navegador (`F12`) para achar erros, muito prático.

## Dificuldades que enfrentei

- Organizar as pastas do projeto, porque acabei com pastas duplicadas e dois ambientes virtuais.
- Descobrir que vários erros eram de digitação, como um `id` escrito com letra maiúscula, que quebrou todo o JavaScript.
- Entender que o terminal fica ocupado enquanto o servidor está rodando.
- Perceber que a senha estava aparecendo na URL quando o JavaScript não carregava,podendo ocorrer falta de segurança.

## Observações
- "Esqueci a senha" e "Cadastre-se" ainda são placeholders.
- Projeto de estudo: o rate limit usa memória e o servidor é o de desenvolvimento.
