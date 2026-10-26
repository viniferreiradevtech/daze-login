const form = document.getElementById('login-form');
const usuario = document.getElementById('usuario');
const senha = document.getElementById('senha');
const lembrar = document.getElementById('lembrar');
const botao = form.querySelector('.login');
const statusMsg = form.querySelector('.form-status');
const toggle = form.querySelector('.toggle-password');

const CHAVE_USUARIO = 'daze:usuario-lembrado';

/* ---------- localStorage seguro ---------- */
function lerStorage(chave) {
    try { return localStorage.getItem(chave); } catch { return null; }
}
function salvarStorage(chave, valor) {
    try { localStorage.setItem(chave, valor); } catch { /* ignora */ }
}
function removerStorage(chave) {
    try { localStorage.removeItem(chave); } catch { /* ignora */ }
}

/* ---------- Restaurar usuário lembrado ---------- */
const usuarioSalvo = lerStorage(CHAVE_USUARIO);
if (usuarioSalvo) {
    usuario.value = usuarioSalvo;
    lembrar.checked = true;
}

/* ---------- Mostrar / ocultar senha ---------- */
toggle.addEventListener('click', () => {
    const mostrando = senha.type === 'text';
    senha.type = mostrando ? 'password' : 'text';

    toggle.setAttribute('aria-pressed', String(!mostrando));
    toggle.setAttribute('aria-label', mostrando ? 'Mostrar senha' : 'Ocultar senha');
    toggle.querySelector('i').className = mostrando ? 'bx bx-show' : 'bx bx-hide';
});

/* ---------- Validação ---------- */
function definirErro(input, mensagem) {
    const campo = input.closest('.field');
    campo.querySelector('.error-message').textContent = mensagem;
    campo.classList.toggle('invalid', Boolean(mensagem));
    input.setAttribute('aria-invalid', String(Boolean(mensagem)));
}

function validarUsuario() {
    if (!usuario.value.trim()) {
        definirErro(usuario, 'Informe seu usuário.');
        return false;
    }
    definirErro(usuario, '');
    return true;
}

function validarSenha() {
    if (!senha.value) {
        definirErro(senha, 'Informe sua senha.');
        return false;
    }
    if (senha.value.length < 6) {
        definirErro(senha, 'A senha deve ter pelo menos 6 caracteres.');
        return false;
    }
    definirErro(senha, '');
    return true;
}

usuario.addEventListener('blur', validarUsuario);
senha.addEventListener('blur', validarSenha);
usuario.addEventListener('input', () => {
    if (usuario.closest('.field').classList.contains('invalid')) validarUsuario();
});
senha.addEventListener('input', () => {
    if (senha.closest('.field').classList.contains('invalid')) validarSenha();
});

/* ---------- Estado de carregamento ---------- */
function carregando(ativo) {
    botao.disabled = ativo;
    botao.classList.toggle('loading', ativo);
    botao.querySelector('.login-text').textContent = ativo ? 'Entrando...' : 'Login';
}

function mostrarStatus(texto, tipo = '') {
    statusMsg.textContent = texto;
    statusMsg.className = `form-status ${tipo}`.trim();
}

/* ---------- Envio ---------- */
form.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    mostrarStatus('');

    const usuarioOk = validarUsuario();
    const senhaOk = validarSenha();

    if (!usuarioOk || !senhaOk) {
        (usuarioOk ? senha : usuario).focus();
        return;
    }

    // Lembra apenas o USUÁRIO. Nunca guarde senha no navegador.
    if (lembrar.checked) {
        salvarStorage(CHAVE_USUARIO, usuario.value.trim());
    } else {
        removerStorage(CHAVE_USUARIO);
    }

    carregando(true);

    try {
        const resposta = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                usuario: usuario.value.trim(),
                senha: senha.value,
                lembrar: lembrar.checked
            })
        });

        const dados = await resposta.json().catch(() => ({}));

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível entrar. Tente novamente.');
        }

        mostrarStatus('Login realizado com sucesso!', 'sucesso');
        window.location.href = dados.redirecionar || '/painel';
    } catch (erro) {
        mostrarStatus(erro.message || 'Não foi possível entrar. Tente novamente.', 'erro');
    } finally {
        carregando(false);
    }
});