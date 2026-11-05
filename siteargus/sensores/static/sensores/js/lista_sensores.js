document.addEventListener("DOMContentLoaded", function () {

    // Elementos da página.
    const listaDispositivos = document.getElementById("lista-dispositivos");
    const totalDispositivos = document.getElementById("total-dispositivos");

    // Elementos do modal.
    const modalExcluir = document.getElementById("modal-excluir");
    const nomeDispositivo = document.getElementById("nome-dispositivo-excluir");
    const botaoCancelar = document.getElementById("cancelar-exclusao");
    const botaoConfirmar = document.getElementById("confirmar-exclusao");

    let formularioSelecionado = null;

    if (!listaDispositivos || !totalDispositivos) {
        return;
    }

    // Abre o modal ao clicar em Excluir.
    listaDispositivos.addEventListener("click", function (evento) {

        const botaoExcluir = evento.target.closest(".botao-excluir");

        if (!botaoExcluir) {
            return;
        }

        formularioSelecionado = botaoExcluir.closest(".form-excluir");

        if (!formularioSelecionado) {
            return;
        }

        nomeDispositivo.textContent = botaoExcluir.dataset.nome;

        modalExcluir.classList.add("ativo");
        modalExcluir.setAttribute("aria-hidden", "false");
    });

    // Fecha o modal.
    function fecharModal() {
        modalExcluir.classList.remove("ativo");
        modalExcluir.setAttribute("aria-hidden", "true");
        formularioSelecionado = null;
    }

    botaoCancelar.addEventListener("click", fecharModal);

    // Fecha ao clicar fora da caixa de confirmação.
    modalExcluir.addEventListener("click", function (evento) {
        if (evento.target === modalExcluir) {
            fecharModal();
        }
    });

    // Confirma e envia o formulário.
    botaoConfirmar.addEventListener("click", function () {

        if (formularioSelecionado) {
            formularioSelecionado.submit();
        }

    });

    // Fecha o modal com a tecla ESC.
    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape" && modalExcluir.classList.contains("ativo")) {
            fecharModal();
        }
    });

    // Atualização automática da lista.
    async function atualizarDispositivos() {

        // Não atualiza em segundo plano nem enquanto o modal está aberto.
        if (
            document.hidden ||
            modalExcluir.classList.contains("ativo")
        ) {
            return;
        }

        try {

            const resposta = await fetch(window.location.href, {
                method: "GET",
                cache: "no-store",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (!resposta.ok) {
                throw new Error("Não foi possível atualizar os dispositivos.");
            }

            const html = await resposta.text();
            const documento = new DOMParser().parseFromString(html, "text/html");

            const novaLista = documento.getElementById("lista-dispositivos");
            const novoTotal = documento.getElementById("total-dispositivos");

            if (novaLista && novoTotal) {
                listaDispositivos.innerHTML = novaLista.innerHTML;
                totalDispositivos.textContent = novoTotal.textContent;
            }

        } catch (erro) {
            console.error("Erro ao atualizar dispositivos:", erro);
        }
    }

    // Atualiza a cada 10 segundos.
    setInterval(atualizarDispositivos, 10000);

});