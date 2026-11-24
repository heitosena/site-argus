
document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // 1. SELETOR DE TEMA
    // =========================================

    const seletorTema = document.getElementById("seletor-tema");

    if (seletorTema) {

        const temaSalvo = localStorage.getItem("tema") || "escuro";

        document.documentElement.setAttribute("data-tema", temaSalvo);
        seletorTema.value = temaSalvo;

        seletorTema.addEventListener("change", function () {

            const novoTema = seletorTema.value;

            document.documentElement.setAttribute("data-tema", novoTema);
            localStorage.setItem("tema", novoTema);

        });
    }


    // =========================================
    // 2. MÁSCARA DOS TELEFONES
    // =========================================

    const camposTelefone = document.querySelectorAll(
        'input[type="tel"]'
    );

    camposTelefone.forEach(function (campo) {

        function aplicarMascara() {

            let numero = campo.value.replace(/\D/g, "");

            numero = numero.substring(0, 11);

            if (numero.length > 10) {

                numero = numero.replace(
                    /^(\d{2})(\d{5})(\d{4}).*/,
                    "($1) $2-$3"
                );

            } else if (numero.length > 6) {

                numero = numero.replace(
                    /^(\d{2})(\d{4})(\d{0,4}).*/,
                    "($1) $2-$3"
                );

            } else if (numero.length > 2) {

                numero = numero.replace(
                    /^(\d{2})(\d+)/,
                    "($1) $2"
                );

            } else if (numero.length > 0) {

                numero = "(" + numero;
            }

            campo.value = numero;
        }

        campo.addEventListener("input", aplicarMascara);

        // Aplica a máscara também nos telefones já cadastrados.
        if (campo.value) {
            aplicarMascara();
        }

    });


    // =========================================
    // 3. DESAPARECIMENTO DAS MENSAGENS
    // =========================================

    const mensagens = document.querySelectorAll(
        ".mensagem-configuracao"
    );

    mensagens.forEach(function (mensagem) {

        setTimeout(function () {

            mensagem.style.transition = "opacity 0.5s ease";
            mensagem.style.opacity = "0";

            setTimeout(function () {
                mensagem.remove();
            }, 500);

        }, 4000);

    });


    // =========================================
    // 4. MODAL DE CONFIRMAÇÃO DE EXCLUSÃO
    // =========================================

    const modalExclusao = document.getElementById("modal-exclusao");
    const mensagemModal = document.getElementById("mensagem-modal-exclusao");
    const contatoModal = document.getElementById("contato-modal-exclusao");

    const botaoCancelar = document.getElementById("cancelar-exclusao");
    const botaoConfirmar = document.getElementById("confirmar-exclusao");

    let formularioSelecionado = null;

    if (
        modalExclusao &&
        mensagemModal &&
        contatoModal &&
        botaoCancelar &&
        botaoConfirmar
    ) {

        document.querySelectorAll(".formulario-excluir-contato").forEach(
            function (formulario) {

                formulario.addEventListener("submit", function (evento) {

                    evento.preventDefault();

                    formularioSelecionado = formulario;

                    const contato = formulario.dataset.contato;
                    const tipo = formulario.dataset.tipo;

                    mensagemModal.textContent =
                        "Tem certeza de que deseja excluir este " + tipo + "?";

                    contatoModal.textContent = contato;

                    modalExclusao.classList.add("ativo");
                    modalExclusao.setAttribute("aria-hidden", "false");

                    botaoCancelar.focus();

                });

            }
        );

        function fecharModalExclusao() {

            modalExclusao.classList.remove("ativo");
            modalExclusao.setAttribute("aria-hidden", "true");

            formularioSelecionado = null;

        }

        botaoCancelar.addEventListener("click", function () {
            fecharModalExclusao();
        });

        botaoConfirmar.addEventListener("click", function () {

            if (formularioSelecionado) {
                formularioSelecionado.submit();
            }

        });

        modalExclusao.addEventListener("click", function (evento) {

            if (evento.target === modalExclusao) {
                fecharModalExclusao();
            }

        });

        document.addEventListener("keydown", function (evento) {

            if (
                evento.key === "Escape" &&
                modalExclusao.classList.contains("ativo")
            ) {
                fecharModalExclusao();
            }

        });

    }


    // =========================================
    // 5. MODAL DE CONFIRMAÇÃO DE SAÍDA
    // =========================================

    const modalSaida = document.getElementById("modal-saida");
    const tituloModalSaida = document.getElementById("titulo-modal-saida");
    const mensagemModalSaida = document.getElementById("mensagem-modal-saida");

    const botaoCancelarSaida = document.getElementById("cancelar-saida");
    const botaoConfirmarSaida = document.getElementById("confirmar-saida");

    let formularioSaidaSelecionado = null;

    if (
        modalSaida &&
        tituloModalSaida &&
        mensagemModalSaida &&
        botaoCancelarSaida &&
        botaoConfirmarSaida
    ) {

        document.querySelectorAll(".formulario-sair-conta").forEach(
            function (formulario) {

                formulario.addEventListener("submit", function (evento) {

                    evento.preventDefault();

                    formularioSaidaSelecionado = formulario;

                    const acao = formulario.dataset.acao;

                    if (acao === "trocar") {

                        tituloModalSaida.textContent = "Trocar de usuário?";

                        mensagemModalSaida.textContent =
                            "Sua sessão atual será encerrada. Depois, você poderá entrar com outra conta.";

                    } else {

                        tituloModalSaida.textContent =
                            "Deseja sair da sua conta?";

                        mensagemModalSaida.textContent =
                            "Sua sessão será encerrada e você retornará à tela de login.";

                    }

                    modalSaida.classList.add("ativo");
                    modalSaida.setAttribute("aria-hidden", "false");

                    botaoCancelarSaida.focus();

                });

            }
        );

        function fecharModalSaida() {

            modalSaida.classList.remove("ativo");
            modalSaida.setAttribute("aria-hidden", "true");

            formularioSaidaSelecionado = null;

        }

        botaoCancelarSaida.addEventListener("click", function () {
            fecharModalSaida();
        });

        botaoConfirmarSaida.addEventListener("click", function () {

            if (formularioSaidaSelecionado) {
                formularioSaidaSelecionado.submit();
            }

        });

        modalSaida.addEventListener("click", function (evento) {

            if (evento.target === modalSaida) {
                fecharModalSaida();
            }

        });

        document.addEventListener("keydown", function (evento) {

            if (
                evento.key === "Escape" &&
                modalSaida.classList.contains("ativo")
            ) {
                fecharModalSaida();
            }

        });

    }

});
