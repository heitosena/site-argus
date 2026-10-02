// Aguarda o carregamento completo do HTML.
document.addEventListener("DOMContentLoaded", function () {

    // Localiza o botão de atualizar.
    const botaoAtualizar = document.getElementById("atualizar-leituras");

    // Verifica se o botão existe.
    if (botaoAtualizar) {

        // Executa uma ação quando o botão é clicado.
        botaoAtualizar.addEventListener("click", function () {

            // Exibe uma mensagem na tela.
            alert("Leituras atualizadas! Não há novos registros.");

        });
    }
});