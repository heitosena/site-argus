
/* =========================================
   A.R.G.U.S. - JAVASCRIPT GLOBAL
   ========================================= */

// Identifica o link correspondente à página atual.
document.addEventListener("DOMContentLoaded", () => {
    const linksMenu = document.querySelectorAll(".menu-lateral a");

    linksMenu.forEach((link) => {
        if (link.classList.contains("ativo")) {
            link.setAttribute("aria-current", "page");
        }
    });
});