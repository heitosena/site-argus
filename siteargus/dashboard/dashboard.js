
/* =========================================
   1. ANIMAÇÃO DOS MEDIDORES CIRCULARES
   ========================================= */

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


/* =========================================
   2. GRÁFICO DO HISTÓRICO DE GÁS
   ========================================= */

/* Desenha o gráfico utilizando os dados enviados pelo Django. */
function desenharGraficoGas() {
    const canvas = document.getElementById("grafico-historico-gas");
    const elementoDados = document.getElementById("historico-gas-dados");

    // Interrompe se os elementos não existirem.
    if (!canvas || !elementoDados) {
        return;
    }

    let leituras = [];

    try {
        leituras = JSON.parse(elementoDados.textContent);
    } catch (erro) {
        console.error("Erro ao carregar o histórico de gás:", erro);
        return;
    }

    // Não desenha o gráfico quando não existem medições.
    if (!leituras || leituras.length === 0) {
        return;
    }

    const contexto = canvas.getContext("2d");

    if (!contexto) {
        return;
    }

    // Obtém o tamanho disponível para o gráfico.
    const largura = canvas.clientWidth;
    const altura = canvas.clientHeight;

    if (!largura || !altura) {
        return;
    }

    // Ajusta a resolução para telas com maior densidade de pixels.
    const escala = window.devicePixelRatio || 1;

    canvas.width = largura * escala;
    canvas.height = altura * escala;

    contexto.setTransform(escala, 0, 0, escala, 0, 0);

    // Limpa o gráfico anterior.
    contexto.clearRect(0, 0, largura, altura);

    // Espaçamento reservado para os eixos.
    const margem = {
        superior: 15,
        inferior: 48,
        esquerda: 42,
        direita: 15
    };

    const larguraGrafico = largura - margem.esquerda - margem.direita;
    const alturaGrafico = altura - margem.superior - margem.inferior;

    if (larguraGrafico <= 0 || alturaGrafico <= 0) {
        return;
    }

    // Converte as leituras em pontos do gráfico.
    const pontos = leituras.map((leitura, indice) => {
        const valor = Math.max(
            0,
            Math.min(Number(leitura.gas_percentual) || 0, 100)
        );

        const x = leituras.length === 1
            ? margem.esquerda + larguraGrafico / 2
            : margem.esquerda + (
                indice / (leituras.length - 1)
            ) * larguraGrafico;

        const y = margem.superior + alturaGrafico - (
            valor / 100
        ) * alturaGrafico;

        return {
            x,
            y,
            valor,
            data: leitura.data_hora
        };
    });

    // Configurações visuais do gráfico.
    contexto.font = "12px Arial";
    contexto.textAlign = "right";
    contexto.textBaseline = "middle";

    // Desenha as linhas horizontais e os valores do eixo vertical.
    for (let valor = 0; valor <= 100; valor += 25) {
        const y = margem.superior + alturaGrafico - (
            valor / 100
        ) * alturaGrafico;

        contexto.beginPath();
        contexto.strokeStyle = "#1a2d40";
        contexto.lineWidth = 1;

        contexto.moveTo(margem.esquerda, y);
        contexto.lineTo(largura - margem.direita, y);
        contexto.stroke();

        contexto.fillStyle = "#5a7a90";

        contexto.fillText(
            `${valor}%`,
            margem.esquerda - 10,
            y
        );
    }

    // Prepara o preenchimento abaixo da linha.
    const gradiente = contexto.createLinearGradient(
        0,
        margem.superior,
        0,
        margem.superior + alturaGrafico
    );

    gradiente.addColorStop(0, "rgba(14, 165, 200, 0.25)");
    gradiente.addColorStop(1, "rgba(14, 165, 200, 0.01)");

    // Desenha a área preenchida.
    if (pontos.length > 1) {
        contexto.beginPath();
        contexto.moveTo(pontos[0].x, margem.superior + alturaGrafico);

        pontos.forEach(ponto => {
            contexto.lineTo(ponto.x, ponto.y);
        });

        contexto.lineTo(
            pontos[pontos.length - 1].x,
            margem.superior + alturaGrafico
        );

        contexto.closePath();
        contexto.fillStyle = gradiente;
        contexto.fill();
    }

    // Desenha a linha principal do gráfico.
    if (pontos.length > 1) {
        contexto.beginPath();

        pontos.forEach((ponto, indice) => {
            if (indice === 0) {
                contexto.moveTo(ponto.x, ponto.y);
            } else {
                contexto.lineTo(ponto.x, ponto.y);
            }
        });

        contexto.strokeStyle = "#0ea5c8";
        contexto.lineWidth = 3;
        contexto.lineJoin = "round";
        contexto.lineCap = "round";
        contexto.stroke();
    }

    // Desenha os pontos de cada medição.
    pontos.forEach(ponto => {
        contexto.beginPath();
        contexto.arc(ponto.x, ponto.y, 4, 0, Math.PI * 2);

        contexto.fillStyle = "#0ea5c8";
        contexto.fill();

        contexto.strokeStyle = "#0d1520";
        contexto.lineWidth = 2;
        contexto.stroke();
    });

    // Formata a data e hora de cada leitura.
    function formatarData(data) {
        if (!data) {
            return "";
        }

        const dataConvertida = new Date(data);

        if (Number.isNaN(dataConvertida.getTime())) {
            return "";
        }

        return dataConvertida.toLocaleString("pt-BR", {
            day: "2-digit",
            month: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
        });
    }

    // Define quantas datas serão exibidas no eixo horizontal.
    const quantidadeEtiquetas = Math.min(pontos.length, 5);

    contexto.font = "11px Arial";
    contexto.fillStyle = "#5a7a90";
    contexto.textAlign = "center";
    contexto.textBaseline = "top";

    for (let indice = 0; indice < quantidadeEtiquetas; indice++) {
        const posicao = quantidadeEtiquetas === 1
            ? 0
            : Math.round(
                indice * (pontos.length - 1) /
                (quantidadeEtiquetas - 1)
            );

        const ponto = pontos[posicao];
        const dataFormatada = formatarData(ponto.data);

        contexto.fillText(
            dataFormatada,
            ponto.x,
            margem.superior + alturaGrafico + 15
        );
    }
}


/* =========================================
   3. INICIALIZAÇÃO DA DASHBOARD
   ========================================= */

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

    // Desenha o histórico de medições.
    desenharGraficoGas();

    // Redesenha o gráfico quando o tamanho da janela mudar.
    window.addEventListener("resize", desenharGraficoGas);
});
