// Aguarda o carregamento completo do HTML.
document.addEventListener("DOMContentLoaded", function () {

    // Localiza o botão de atualizar.
    const botaoAtualizar = document.getElementById("atualizar-leituras");

    // Verifica se o botão existe.
    if (botaoAtualizar) {

        // Executa uma ação quando o botão é clicado.
        botaoAtualizar.addEventListener("click", function () {

            // Recarrega a página para buscar as leituras mais recentes.
            window.location.reload();

        });
    }

    // Localiza o botão de excluir.
    const botaoExcluir = document.getElementById("excluir-leituras");

    // Verifica se o botão existe.
    if (botaoExcluir) {

        // Exibe uma confirmação antes de excluir.
        botaoExcluir.addEventListener("click", function (event) {

            // Pergunta se o usuário realmente deseja excluir.
            const confirmar = confirm(
                "Tem certeza que deseja excluir as leituras selecionadas?"
            );

            // Cancela a exclusão caso o usuário escolha cancelar.
            if (!confirmar) {
                event.preventDefault();
            }

        });
    }

});