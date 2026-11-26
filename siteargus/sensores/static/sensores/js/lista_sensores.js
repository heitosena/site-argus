
document.addEventListener("DOMContentLoaded", function () {

    // Elementos da página.
    const listaDispositivos = document.getElementById("lista-dispositivos");
    const totalDispositivos = document.getElementById("total-dispositivos");

    // Elementos do modal de exclusão.
    const modalExcluir = document.getElementById("modal-excluir");
    const nomeDispositivo = document.getElementById("nome-dispositivo-excluir");
    const botaoCancelar = document.getElementById("cancelar-exclusao");
    const botaoConfirmar = document.getElementById("confirmar-exclusao");

    // Elementos do modal de confirmação de edição.
    const modalConfirmarEdicao = document.getElementById("modal-confirmar-edicao");
    const nomeDispositivoEditar = document.getElementById("nome-dispositivo-editar");
    const botaoCancelarConfirmacao = document.getElementById("cancelar-confirmacao-edicao");
    const botaoConfirmarEdicao = document.getElementById("confirmar-edicao");

    // Elementos do modal de edição.
    const modalEditar = document.getElementById("modal-editar");
    const formularioEditar = document.getElementById("form-editar");
    const nomeEditar = document.getElementById("nome-editar");
    const redeEditar = document.getElementById("rede-editar");
    const botaoCancelarEdicao = document.getElementById("cancelar-edicao");

    let formularioSelecionado = null;
    let dispositivoSelecionado = null;

    // Mensagem de sucesso.
    const mensagemSucesso = document.getElementById("mensagem-sucesso");

    // Faz a mensagem desaparecer após 10 segundos.
    if (mensagemSucesso) {

        setTimeout(function () {

            mensagemSucesso.style.transition = "opacity 0.5s";
            mensagemSucesso.style.opacity = "0";

            setTimeout(function () {
                mensagemSucesso.remove();
            }, 500);

        }, 10000);

    }

document.addEventListener("DOMContentLoaded", function () {

    // Elementos da página.
    const listaDispositivos = document.getElementById("lista-dispositivos");
    const totalDispositivos = document.getElementById("total-dispositivos");

    // Elementos do modal de exclusão.
    const modalExcluir = document.getElementById("modal-excluir");
    const nomeDispositivo = document.getElementById("nome-dispositivo-excluir");
    const botaoCancelar = document.getElementById("cancelar-exclusao");
    const botaoConfirmar = document.getElementById("confirmar-exclusao");

    // Elementos do modal de confirmação de edição.
    const modalConfirmarEdicao = document.getElementById("modal-confirmar-edicao");
    const nomeDispositivoEditar = document.getElementById("nome-dispositivo-editar");
    const botaoCancelarConfirmacao = document.getElementById("cancelar-confirmacao-edicao");
    const botaoConfirmarEdicao = document.getElementById("confirmar-edicao");

    // Elementos do modal de edição.
    const modalEditar = document.getElementById("modal-editar");
    const formularioEditar = document.getElementById("form-editar");
    const nomeEditar = document.getElementById("nome-editar");
    const statusEditar = document.getElementById("status-editar");
    const redeEditar = document.getElementById("rede-editar");
    const botaoCancelarEdicao = document.getElementById("cancelar-edicao");

    let formularioSelecionado = null;
    let dispositivoSelecionado = null;

    // Mensagem de sucesso.
    const mensagemSucesso = document.getElementById("mensagem-sucesso");

    // Faz a mensagem desaparecer após 10 segundos.
    if (mensagemSucesso) {

        setTimeout(function () {

            mensagemSucesso.style.transition = "opacity 0.5s";
            mensagemSucesso.style.opacity = "0";

            setTimeout(function () {
                mensagemSucesso.remove();
            }, 500);

        }, 10000);

    }

    if (!listaDispositivos || !totalDispositivos) {
        return;
    }

    // Abre os modais de confirmação de edição ou exclusão.
    listaDispositivos.addEventListener("click", function (evento) {

        // Verifica se o botão clicado foi Editar.
        const botaoEditar = evento.target.closest(".botao-editar");

        if (botaoEditar) {

            dispositivoSelecionado = botaoEditar;

            nomeDispositivoEditar.textContent = botaoEditar.dataset.nome;

            modalConfirmarEdicao.classList.add("ativo");
            modalConfirmarEdicao.setAttribute("aria-hidden", "false");

            return;
        }

        // Verifica se o botão clicado foi Excluir.
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

    // Fecha o modal de exclusão.
    function fecharModalExcluir() {
        modalExcluir.classList.remove("ativo");
        modalExcluir.setAttribute("aria-hidden", "true");
        formularioSelecionado = null;
    }

    botaoCancelar.addEventListener("click", fecharModalExcluir);

    // Fecha o modal de confirmação de edição.
    function fecharModalConfirmarEdicao() {
        modalConfirmarEdicao.classList.remove("ativo");
        modalConfirmarEdicao.setAttribute("aria-hidden", "true");
        dispositivoSelecionado = null;
    }

    botaoCancelarConfirmacao.addEventListener("click", fecharModalConfirmarEdicao);

    // Confirma a edição e abre o formulário.
    botaoConfirmarEdicao.addEventListener("click", function () {

        if (!dispositivoSelecionado) {
            return;
        }

        formularioEditar.action = dispositivoSelecionado.dataset.url;
        nomeEditar.value = dispositivoSelecionado.dataset.nome;
        statusEditar.value = dispositivoSelecionado.dataset.status;
        redeEditar.checked = dispositivoSelecionado.dataset.rede === "true";

        fecharModalConfirmarEdicao();

        modalEditar.classList.add("ativo");
        modalEditar.setAttribute("aria-hidden", "false");

        nomeEditar.focus();

    });

    // Fecha o modal de edição.
    function fecharModalEditar() {
        modalEditar.classList.remove("ativo");
        modalEditar.setAttribute("aria-hidden", "true");
    }

    botaoCancelarEdicao.addEventListener("click", fecharModalEditar);

    // Fecha os modais ao clicar fora da caixa.
    modalExcluir.addEventListener("click", function (evento) {

        if (evento.target === modalExcluir) {
            fecharModalExcluir();
        }

    });

    modalConfirmarEdicao.addEventListener("click", function (evento) {

        if (evento.target === modalConfirmarEdicao) {
            fecharModalConfirmarEdicao();
        }

    });

    modalEditar.addEventListener("click", function (evento) {

        if (evento.target === modalEditar) {
            fecharModalEditar();
        }

    });

    // Confirma e envia o formulário de exclusão.
    botaoConfirmar.addEventListener("click", function () {

        if (formularioSelecionado) {
            formularioSelecionado.submit();
        }

    });

    // Fecha os modais com a tecla ESC.
    document.addEventListener("keydown", function (evento) {

        if (evento.key === "Escape") {

            if (modalExcluir.classList.contains("ativo")) {
                fecharModalExcluir();
            }

            if (modalConfirmarEdicao.classList.contains("ativo")) {
                fecharModalConfirmarEdicao();
            }

            if (modalEditar.classList.contains("ativo")) {
                fecharModalEditar();
            }

        }

    });

    // Atualização automática da lista.
    async function atualizarDispositivos() {

        // Não atualiza em segundo plano nem enquanto algum modal está aberto.
        if (
            document.hidden ||
            modalExcluir.classList.contains("ativo") ||
            modalConfirmarEdicao.classList.contains("ativo") ||
            modalEditar.classList.contains("ativo")
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

    // Atualiza a cada 4 segundos.
    setInterval(atualizarDispositivos, 4000);

});

    if (!listaDispositivos || !totalDispositivos) {
        return;
    }

    // Abre os modais de confirmação de edição ou exclusão.
    listaDispositivos.addEventListener("click", function (evento) {

        // Verifica se o botão clicado foi Editar.
        const botaoEditar = evento.target.closest(".botao-editar");

        if (botaoEditar) {

            dispositivoSelecionado = botaoEditar;

            nomeDispositivoEditar.textContent = botaoEditar.dataset.nome;

            modalConfirmarEdicao.classList.add("ativo");
            modalConfirmarEdicao.setAttribute("aria-hidden", "false");

            return;
        }

        // Verifica se o botão clicado foi Excluir.
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

    // Fecha o modal de exclusão.
    function fecharModalExcluir() {
        modalExcluir.classList.remove("ativo");
        modalExcluir.setAttribute("aria-hidden", "true");
        formularioSelecionado = null;
    }

    botaoCancelar.addEventListener("click", fecharModalExcluir);

    // Fecha o modal de confirmação de edição.
    function fecharModalConfirmarEdicao() {
        modalConfirmarEdicao.classList.remove("ativo");
        modalConfirmarEdicao.setAttribute("aria-hidden", "true");
        dispositivoSelecionado = null;
    }

    botaoCancelarConfirmacao.addEventListener("click", fecharModalConfirmarEdicao);

    // Confirma a edição e abre o formulário.
    botaoConfirmarEdicao.addEventListener("click", function () {

        if (!dispositivoSelecionado) {
            return;
        }

        formularioEditar.action = dispositivoSelecionado.dataset.url;
        nomeEditar.value = dispositivoSelecionado.dataset.nome;
        redeEditar.checked = dispositivoSelecionado.dataset.rede === "true";

        fecharModalConfirmarEdicao();

        modalEditar.classList.add("ativo");
        modalEditar.setAttribute("aria-hidden", "false");

        nomeEditar.focus();

    });

    // Fecha o modal de edição.
    function fecharModalEditar() {
        modalEditar.classList.remove("ativo");
        modalEditar.setAttribute("aria-hidden", "true");
    }

    botaoCancelarEdicao.addEventListener("click", fecharModalEditar);

    // Fecha os modais ao clicar fora da caixa.
    modalExcluir.addEventListener("click", function (evento) {

        if (evento.target === modalExcluir) {
            fecharModalExcluir();
        }

    });

    modalConfirmarEdicao.addEventListener("click", function (evento) {

        if (evento.target === modalConfirmarEdicao) {
            fecharModalConfirmarEdicao();
        }

    });

    modalEditar.addEventListener("click", function (evento) {

        if (evento.target === modalEditar) {
            fecharModalEditar();
        }

    });

    // Confirma e envia o formulário de exclusão.
    botaoConfirmar.addEventListener("click", function () {

        if (formularioSelecionado) {
            formularioSelecionado.submit();
        }

    });

    // Fecha os modais com a tecla ESC.
    document.addEventListener("keydown", function (evento) {

        if (evento.key === "Escape") {

            if (modalExcluir.classList.contains("ativo")) {
                fecharModalExcluir();
            }

            if (modalConfirmarEdicao.classList.contains("ativo")) {
                fecharModalConfirmarEdicao();
            }

            if (modalEditar.classList.contains("ativo")) {
                fecharModalEditar();
            }

        }

    });

    // Atualização automática da lista.
    async function atualizarDispositivos() {

        // Não atualiza em segundo plano nem enquanto algum modal está aberto.
        if (
            document.hidden ||
            modalExcluir.classList.contains("ativo") ||
            modalConfirmarEdicao.classList.contains("ativo") ||
            modalEditar.classList.contains("ativo")
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
    setInterval(atualizarDispositivos, 4000);

});
