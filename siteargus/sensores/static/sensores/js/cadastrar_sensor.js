document.addEventListener("DOMContentLoaded", function () {

    // Elementos do formulário.
    const formulario = document.querySelector("form");
    const campoNome = document.getElementById("nome");
    const botaoCadastrar = formulario?.querySelector('button[type="submit"]');

    // Verifica se os elementos existem.
    if (!formulario || !campoNome || !botaoCadastrar) {
        return;
    }

    // Restaura o botão ao carregar a página.
    botaoCadastrar.disabled = false;
    botaoCadastrar.textContent = "Cadastrar Dispositivo";

    // Identifica a mensagem de sucesso.
    const mensagemSucesso = document.querySelector(".mensagem-sucesso");

    // Limpa o formulário depois de um cadastro bem-sucedido.
    if (mensagemSucesso) {
        formulario.reset();

        // Faz a mensagem desaparecer após 4 segundos.
        setTimeout(function () {

            mensagemSucesso.style.transition = "opacity 0.5s";
            mensagemSucesso.style.opacity = "0";

            // Remove a mensagem depois da animação.
            setTimeout(function () {
                mensagemSucesso.remove();
            }, 500);

        }, 4000);
    }

    // Validação antes de enviar o formulário.
    formulario.addEventListener("submit", function (evento) {

        const nome = campoNome.value.trim();

        // Verifica o nome.
        if (nome.length < 2) {
            evento.preventDefault();
            alert("Digite um nome válido para o dispositivo.");
            campoNome.focus();
            return;
        }

        // Evita múltiplos envios.
        botaoCadastrar.disabled = true;
        botaoCadastrar.textContent = "Cadastrando...";

    });

});