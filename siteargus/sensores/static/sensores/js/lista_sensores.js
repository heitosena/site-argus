document.addEventListener("DOMContentLoaded", function () {

    // Elementos da página.
    const listaDispositivos = document.getElementById("lista-dispositivos");
    const totalDispositivos = document.getElementById("total-dispositivos");

    // Verifica se os elementos existem.
    if (!listaDispositivos || !totalDispositivos) {
        return;
    }

    // Atualiza a lista consultando novamente o servidor.
    async function atualizarDispositivos() {

        // Não atualiza enquanto a página estiver em segundo plano.
        if (document.hidden) {
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

            // Recebe o HTML atualizado.
            const html = await resposta.text();

            // Transforma a resposta em um documento HTML.
            const documento = new DOMParser().parseFromString(html, "text/html");

            // Busca os elementos atualizados.
            const novaLista = documento.getElementById("lista-dispositivos");
            const novoTotal = documento.getElementById("total-dispositivos");

            // Atualiza a página.
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