
const formularioCadastro = document.getElementById("formCad");

const nome = document.getElementById("nome");
const email = document.getElementById("email");
const senha = document.getElementById("senha");
const confSenha = document.getElementById("confSenha");
const telefone = document.getElementById("telefone");

// Função para mostrar mensagens de erro.
function mostrarErro(campo, mensagem) {
    campo.classList.add("campoInvalido");

    const mensagemErro = document.createElement("span");
    mensagemErro.classList.add("mensagemErro");
    mensagemErro.textContent = mensagem;

    campo.insertAdjacentElement("afterend", mensagemErro);
}

// Função para limpar mensagens de erro.
function limparErros() {
    document.querySelectorAll(".mensagemErro").forEach(erro => {
        erro.remove();
    });

    document.querySelectorAll(".campoInvalido").forEach(campo => {
        campo.classList.remove("campoInvalido");
    });
}

// Máscara e formatação do telefone.
telefone.addEventListener("input", function() {

    let valor = telefone.value.replace(/\D/g, "");

    if (valor.length > 11) {
        valor = valor.substring(0, 11);
    }

    if (valor.length > 6) {
        telefone.value = "(" + valor.substring(0, 2) + ") "
            + valor.substring(2, 7) + "-"
            + valor.substring(7);
    }
    else if (valor.length > 2) {
        telefone.value = "(" + valor.substring(0, 2) + ") "
            + valor.substring(2);
    }
    else {
        telefone.value = valor;
    }
});

// Remove os erros quando o usuário começa a corrigir os campos.
formularioCadastro.querySelectorAll("input").forEach(campo => {
    campo.addEventListener("input", function() {
        campo.classList.remove("campoInvalido");

        const proximaMensagem = campo.nextElementSibling;

        if (proximaMensagem &&
            proximaMensagem.classList.contains("mensagemErro")) {
            proximaMensagem.remove();
        }
    });
});

// Validação do formulário.
formularioCadastro.addEventListener("submit", function(event) {

    limparErros();

    let formularioValido = true;
    let primeiroErro = null;

    function validar(campo, condicao, mensagem) {
        if (!condicao) {
            mostrarErro(campo, mensagem);
            formularioValido = false;

            if (!primeiroErro) {
                primeiroErro = campo;
            }
        }
    }

    // Validação do nome.
    validar(
        nome,
        nome.value.trim().length >= 7,
        "Digite seu nome completo."
    );

    // Validação do e-mail.
    const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());

    validar(
        email,
        emailValido,
        "Digite um e-mail válido."
    );

    // Validação da senha.
    validar(
        senha,
        senha.value.length >= 8,
        "A senha deve ter no mínimo 8 caracteres."
    );

    // Confirmação da senha.
    validar(
        confSenha,
        confSenha.value === senha.value && confSenha.value !== "",
        "As duas senhas devem ser iguais."
    );

    // Validação do telefone.
    const numeroTelefone = telefone.value.replace(/\D/g, "");

    validar(
        telefone,
        numeroTelefone.length === 10 || numeroTelefone.length === 11,
        "Digite um telefone válido."
    );

    // Impede o envio se houver algum erro.
    if (!formularioValido) {
        event.preventDefault();
        primeiroErro.focus();
    }

    // Se estiver tudo correto, o formulário é enviado
    // normalmente para o Django.
});
