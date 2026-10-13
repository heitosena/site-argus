/* Anima um medidor circular do valor inicial até o valor final. */
function animarMedidor(id, valorFinal, valorMaximo, unidade = "") {
    const medidor = document.getElementById(id);

    // Interrompe a função se o medidor não existir na página.
    if (!medidor) {
        return;
    }

    const textoValor = medidor.querySelector(".valor-medidor");

    // Evita valores negativos ou acima do limite definido.
    const valorDestino = Math.max(
        0,
        Math.min(valorFinal, valorMaximo)
    );

    const duracao = 1200;
    const inicio = performance.now();

    // Atualiza o número e o preenchimento do círculo.
    function atualizar(instanteAtual) {
        const tempoDecorrido = instanteAtual - inicio;
        const progresso = Math.min(tempoDecorrido / duracao, 1);

        // Suaviza a animação para não começar nem terminar bruscamente.
        const suavizacao = 1 - Math.pow(1 - progresso, 3);

        const valorAtual = valorDestino * suavizacao;
        const angulo = (valorAtual / valorMaximo) * 360;

        textoValor.textContent = `${Math.round(valorAtual)}${unidade}`;

        medidor.style.setProperty("--progresso", `${angulo}deg`);

        // Continua a animação até atingir o valor final.
        if (progresso < 1) {
            requestAnimationFrame(atualizar);
        }
    }

    // Começa a animação.
    requestAnimationFrame(atualizar);
}

/* Executa uma animação de teste ao abrir a Dashboard. */
document.addEventListener("DOMContentLoaded", function () {
    animarMedidor("medidor-temperatura", 28, 50);
    animarMedidor("medidor-umidade", 60, 100);
    animarMedidor("medidor-gas", 35, 100, "%");
    animarMedidor("medidor-bateria", 85, 100, "%");
});