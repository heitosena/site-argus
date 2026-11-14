
document.addEventListener("DOMContentLoaded", function () {

    // Elementos do formulário.
    const formulario = document.querySelector(".pagina-cadastro form");
    const campoNome = document.getElementById("nome");
    const botaoCadastrar = formulario?.querySelector('button[type="submit"]');

    // Verifica se os elementos existem.
    if (!formulario || !campoNome || !botaoCadastrar) {
        return;
    }

    // Restaura o botão ao carregar a página.
    botaoCadastrar.disabled = false;
    botaoCadastrar.textContent = "Cadastrar dispositivo";

    // Mensagem de sucesso do cadastro.
    const mensagemSucesso = document.querySelector(".mensagem-sucesso");

    // Faz a mensagem desaparecer após 4 segundos.
    if (mensagemSucesso) {

        setTimeout(function () {

            mensagemSucesso.style.transition = "opacity 0.5s";
            mensagemSucesso.style.opacity = "0";

            setTimeout(function () {
                mensagemSucesso.remove();
            }, 500);

        }, 4000);

    }

    // Adiciona a borda vermelha quando o navegador identifica um campo inválido.
    campoNome.addEventListener("invalid", function () {
        campoNome.classList.add("campoInvalido");
    });

    // Remove a validação quando o usuário começa a corrigir o nome.
    campoNome.addEventListener("input", function () {

        campoNome.setCustomValidity("");

        if (campoNome.value.trim().length >= 2) {
            campoNome.classList.remove("campoInvalido");
        }

    });

    // Validação antes de enviar o formulário.
    formulario.addEventListener("submit", function (evento) {

        const nome = campoNome.value.trim();

        if (nome.length < 2) {

            evento.preventDefault();

            campoNome.classList.add("campoInvalido");
            campoNome.setCustomValidity("Preencha este campo.");
            campoNome.reportValidity();

            return;
        }

        campoNome.setCustomValidity("");
        campoNome.classList.remove("campoInvalido");

        // Evita múltiplos envios.
        botaoCadastrar.disabled = true;
        botaoCadastrar.textContent = "Cadastrando...";

    });

});
