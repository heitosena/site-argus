
/* Anima um medidor circular do valor inicial até o valor final. */
function animarMedidor(id, valorFinal, valorMaximo, unidade = "") {
    const medidor = document.getElementById(id);

    // Interrompe a função se o medidor não existir na página.
    if (!medidor) {
        return;
    }

    const textoValor = medidor.querySelector(".valor-medidor");

    // Interrompe se o elemento do valor não existir.
    if (!textoValor) {
        return;
    }

    // Evita valores negativos ou acima do limite definido.
    const valorDestino = Math.max(
        0,
        Math.min(valorFinal, valorMaximo)
    );

    const duracao = 1200;
    const inicio = performance.now();

    // Define quantas casas decimais cada medidor deve apresentar.
    const casasDecimais = (
        id === "medidor-temperatura" ||
        id === "medidor-umidade"
    ) ? 1 : 0;

    // Atualiza o número e o preenchimento do círculo.
    function atualizar(instanteAtual) {
        const tempoDecorrido = instanteAtual - inicio;
        const progresso = Math.min(tempoDecorrido / duracao, 1);

        // Suaviza a animação para não começar nem terminar bruscamente.
        const suavizacao = 1 - Math.pow(1 - progresso, 3);

        const valorAtual = valorDestino * suavizacao;
        const angulo = (valorAtual / valorMaximo) * 360;

        // Formata o valor conforme o tipo de medidor.
        textoValor.textContent = `${valorAtual.toLocaleString("pt-BR", {
            minimumFractionDigits: casasDecimais,
            maximumFractionDigits: casasDecimais
        })}${unidade}`;

        medidor.style.setProperty("--progresso", `${angulo}deg`);

        // Continua a animação até atingir o valor final.
        if (progresso < 1) {
            requestAnimationFrame(atualizar);
        }
    }

    // Começa a animação.
    requestAnimationFrame(atualizar);
}


/* Executa os medidores usando os valores enviados pelo Django. */
document.addEventListener("DOMContentLoaded", function () {

    // Busca cada medidor da página.
    const temperatura = document.getElementById("medidor-temperatura");
    const umidade = document.getElementById("medidor-umidade");
    const gas = document.getElementById("medidor-gas");
    const bateria = document.getElementById("medidor-bateria");

    // Anima o medidor de temperatura com o valor do banco.
    animarMedidor(
        "medidor-temperatura",
        parseFloat(temperatura?.dataset.valor) || 0,
        50,
        " °C"
    );

    // Anima o medidor de umidade com o valor do banco.
    animarMedidor(
        "medidor-umidade",
        parseFloat(umidade?.dataset.valor) || 0,
        100,
        "%"
    );

    // Anima o medidor de gás com o valor do banco.
    animarMedidor(
        "medidor-gas",
        parseFloat(gas?.dataset.valor) || 0,
        100,
        "%"
    );

    // Anima o medidor da bateria com o valor do dispositivo.
    animarMedidor(
        "medidor-bateria",
        parseFloat(bateria?.dataset.valor) || 0,
        100,
        "%"
    );
});