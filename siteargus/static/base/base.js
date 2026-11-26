
document.addEventListener("DOMContentLoaded", () => {

    // =========================================
    // MENU LATERAL
    // =========================================

    const linksMenu = document.querySelectorAll(".menu-lateral a");

    linksMenu.forEach((link) => {
        if (link.classList.contains("ativo")) {
            link.setAttribute("aria-current", "page");
        }
    });


    // =========================================
    // TEMA CLARO E ESCURO
    // =========================================

    const seletorTema = document.getElementById("seletor-tema");

    let temaAtual = localStorage.getItem("argus-tema") || "escuro";

    document.documentElement.setAttribute("data-tema", temaAtual);

    if (seletorTema) {

        // BOTÃO DA NAVBAR (VISITANTES)
        if (seletorTema.tagName === "BUTTON") {

            const atualizarIcone = () => {
                seletorTema.textContent = temaAtual === "escuro" ? "☀" : "☾";
            };

            atualizarIcone();

            seletorTema.addEventListener("click", () => {

                temaAtual = temaAtual === "escuro" ? "claro" : "escuro";

                document.documentElement.setAttribute("data-tema", temaAtual);

                localStorage.setItem("argus-tema", temaAtual);

                atualizarIcone();

            });

        }

        // SELETOR DAS CONFIGURAÇÕES (USUÁRIOS LOGADOS)
        else if (seletorTema.tagName === "SELECT") {

            seletorTema.value = temaAtual;

            seletorTema.addEventListener("change", () => {

                temaAtual = seletorTema.value;

                document.documentElement.setAttribute("data-tema", temaAtual);

                localStorage.setItem("argus-tema", temaAtual);

            });

        }
    }


    // =========================================
    // MENU DO PERFIL
    // =========================================

    const botaoPerfil = document.getElementById("perfil-menu-botao");
    const menuPerfil = document.getElementById("perfil-menu");

    if (botaoPerfil && menuPerfil) {

        botaoPerfil.addEventListener("click", (event) => {
            event.stopPropagation();

            const aberto = menuPerfil.classList.toggle("aberto");

            botaoPerfil.setAttribute("aria-expanded", aberto);
        });

        // Fecha ao clicar fora do menu
        document.addEventListener("click", (event) => {
            if (
                !menuPerfil.contains(event.target) &&
                !botaoPerfil.contains(event.target)
            ) {
                menuPerfil.classList.remove("aberto");
                botaoPerfil.setAttribute("aria-expanded", "false");
            }
        });

        // Fecha com ESC
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                menuPerfil.classList.remove("aberto");
                botaoPerfil.setAttribute("aria-expanded", "false");
            }
        });
    }


    // =========================================
    // MODAL DE CONFIRMAÇÃO DE SAÍDA
    // =========================================

    const modalConfirmacao = document.getElementById("modal-confirmacao");
    const modalTitulo = document.getElementById("modal-titulo");
    const modalMensagem = document.getElementById("modal-mensagem");

    const botaoCancelar = document.getElementById("modal-cancelar");
    const botaoConfirmar = document.getElementById("modal-confirmar");

    const linksSaida = document.querySelectorAll(
        ".perfil-menu a[data-confirmacao]"
    );

    let destinoSaida = null;

    if (
        modalConfirmacao &&
        modalTitulo &&
        modalMensagem &&
        botaoCancelar &&
        botaoConfirmar
    ) {

        // Abre o modal conforme a opção escolhida
        linksSaida.forEach((link) => {

            link.addEventListener("click", (event) => {
                event.preventDefault();

                destinoSaida = link.href;

                const acao = link.dataset.confirmacao;

                if (acao === "trocar") {
                    modalTitulo.textContent = "Deseja trocar de conta?";

                    modalMensagem.textContent =
                        "Sua sessão atual será encerrada e você será redirecionado para a tela de login.";

                } else {
                    modalTitulo.textContent = "Deseja sair da sua conta?";

                    modalMensagem.textContent =
                        "Sua sessão será encerrada e você retornará à tela de login.";
                }

                modalConfirmacao.classList.add("aberto");

                // Fecha o menu do perfil
                if (menuPerfil) {
                    menuPerfil.classList.remove("aberto");
                }

                if (botaoPerfil) {
                    botaoPerfil.setAttribute("aria-expanded", "false");
                }

                botaoCancelar.focus();
            });

        });


        // Fecha o modal
        function fecharModal() {
            modalConfirmacao.classList.remove("aberto");
            destinoSaida = null;
        }


        // Botão Não
        botaoCancelar.addEventListener("click", () => {
            fecharModal();
        });


        // Botão Sim
        botaoConfirmar.addEventListener("click", () => {

            if (destinoSaida) {
                window.location.href = destinoSaida;
            }

        });


        // Fecha ao clicar fora da caixa
        modalConfirmacao.addEventListener("click", (event) => {

            if (event.target === modalConfirmacao) {
                fecharModal();
            }

        });


        // Fecha com ESC
        document.addEventListener("keydown", (event) => {

            if (
                event.key === "Escape" &&
                modalConfirmacao.classList.contains("aberto")
            ) {
                fecharModal();
            }

        });

    }

});
