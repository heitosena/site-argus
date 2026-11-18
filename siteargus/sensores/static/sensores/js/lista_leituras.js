// Aguarda o carregamento completo do HTML.
document.addEventListener("DOMContentLoaded", function () {

    // Botão para atualizar as leituras.
    const botaoAtualizar = document.getElementById("atualizar-leituras");

    if (botaoAtualizar) {
        botaoAtualizar.addEventListener("click", function () {
            window.location.reload();
        });
    }

    // Localiza os elementos de exclusão.
    const botaoExcluir = document.getElementById("excluir-leituras");
    const formulario = botaoExcluir?.closest("form");

    // Modais.
    const modalExclusao = document.getElementById("modal-exclusao");
    const modalAviso = document.getElementById("modal-aviso");

    // Botões dos modais.
    const cancelarExclusao = document.getElementById("cancelar-exclusao");
    const confirmarExclusao = document.getElementById("confirmar-exclusao");
    const fecharAviso = document.getElementById("fechar-aviso");

    // Abre um modal.
    function abrirModal(modal) {
        if (modal) {
            modal.classList.add("ativo");
            modal.setAttribute("aria-hidden", "false");
        }
    }

    // Fecha um modal.
    function fecharModal(modal) {
        if (modal) {
            modal.classList.remove("ativo");
            modal.setAttribute("aria-hidden", "true");
        }
    }

    // Verifica se os elementos necessários existem.
    if (botaoExcluir && formulario) {

        // Intercepta o clique no botão Excluir.
        botaoExcluir.addEventListener("click", function (event) {

            event.preventDefault();

            // Conta as leituras selecionadas.
            const selecionadas = formulario.querySelectorAll(
                'input[name="registros"]:checked'
            );

            // Exibe o aviso se nenhuma leitura estiver selecionada.
            if (selecionadas.length === 0) {
                abrirModal(modalAviso);
                return;
            }

            // Exibe a confirmação personalizada.
            abrirModal(modalExclusao);
        });

        // Cancela a exclusão.
        if (cancelarExclusao) {
            cancelarExclusao.addEventListener("click", function () {
                fecharModal(modalExclusao);
            });
        }

        // Confirma a exclusão.
        if (confirmarExclusao) {
            confirmarExclusao.addEventListener("click", function () {

                // Mantém a rota específica do botão Excluir.
                formulario.action = botaoExcluir.getAttribute("formaction");

                // Envia o formulário por POST.
                formulario.submit();
            });
        }
    }

    // Fecha o aviso de seleção vazia.
    if (fecharAviso) {
        fecharAviso.addEventListener("click", function () {
            fecharModal(modalAviso);
        });
    }

    // Fecha os modais ao clicar fora da caixa.
    [modalExclusao, modalAviso].forEach(function (modal) {

        if (modal) {
            modal.addEventListener("click", function (event) {

                if (event.target === modal) {
                    fecharModal(modal);
                }

            });
        }

    });

    // Fecha os modais com a tecla Escape.
    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            fecharModal(modalExclusao);
            fecharModal(modalAviso);
        }

    });

});