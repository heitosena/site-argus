
/* =========================================
   A.R.G.U.S. - JAVASCRIPT GLOBAL
   ========================================= */

document.addEventListener("DOMContentLoaded", () => {

    // Identifica o link correspondente à página atual.
    const linksMenu = document.querySelectorAll(".menu-lateral a");

    linksMenu.forEach((link) => {
        if (link.classList.contains("ativo")) {
            link.setAttribute("aria-current", "page");
        }
    });

    // =========================================
    // CONFIGURAÇÃO DO TEMA
    // =========================================

    const seletorTema = document.getElementById("seletor-tema");

    // Recupera o tema salvo no navegador.
    const temaSalvo = localStorage.getItem("argus-tema");

    // Define o tema inicial.
    const temaInicial = temaSalvo === "claro" ? "claro" : "escuro";

    document.documentElement.setAttribute("data-tema", temaInicial);

    // Atualiza o seletor quando estiver na página de configurações.
    if (seletorTema) {

        seletorTema.value = temaInicial;

        seletorTema.addEventListener("change", () => {

            const novoTema = seletorTema.value;

            document.documentElement.setAttribute("data-tema", novoTema);

            // Salva a preferência no navegador.
            localStorage.setItem("argus-tema", novoTema);

        });
    }

});
