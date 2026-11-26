
/* =========================================
   1. ANIMAÇÃO DOS MEDIDORES CIRCULARES
   ========================================= */

function animarMedidor(id, valorFinal, valorMaximo, unidade = "") {
    const medidor = document.getElementById(id);

    if (!medidor) {
        return;
    }

    const textoValor = medidor.querySelector(".valor-medidor");

    if (!textoValor) {
        return;
    }

    const valorDestino = Math.max(
        0,
        Math.min(Number(valorFinal) || 0, valorMaximo)
    );

    // Recupera o último valor exibido.
    const valorInicial = Number(medidor.dataset.valorAtual) || 0;

    const duracao = 1200;
    const inicio = performance.now();

    const casasDecimais = (
        id === "medidor-temperatura" ||
        id === "medidor-umidade"
    ) ? 1 : 0;

    function atualizar(instanteAtual) {
        const tempoDecorrido = instanteAtual - inicio;
        const progresso = Math.min(tempoDecorrido / duracao, 1);

        const suavizacao = 1 - Math.pow(1 - progresso, 3);

        const valorAtual = valorInicial + (
            (valorDestino - valorInicial) * suavizacao
        );

        const angulo = (valorAtual / valorMaximo) * 360;

        textoValor.textContent = `${valorAtual.toLocaleString("pt-BR", {
            minimumFractionDigits: casasDecimais,
            maximumFractionDigits: casasDecimais
        })}${unidade}`;

        medidor.style.setProperty("--progresso", `${angulo}deg`);

        medidor.dataset.valorAtual = valorAtual;

        if (progresso < 1) {
            requestAnimationFrame(atualizar);
        } else {
            medidor.dataset.valorAtual = valorDestino;
        }
    }

    requestAnimationFrame(atualizar);
}


/* =========================================
   2. HISTÓRICO DE MEDIÇÕES
   ========================================= */

// Guarda os dados recebidos pela API.
let historicoGas = [];


/* Desenha o gráfico utilizando os dados disponíveis. */
function desenharGraficoGas() {
    const canvas = document.getElementById("grafico-historico-gas");

    if (!canvas) {
        return;
    }

    const contexto = canvas.getContext("2d");

    if (!contexto) {
        return;
    }

    const largura = canvas.clientWidth;
    const altura = canvas.clientHeight;

    if (!largura || !altura) {
        return;
    }

    const escala = window.devicePixelRatio || 1;

    canvas.width = largura * escala;
    canvas.height = altura * escala;

    contexto.setTransform(escala, 0, 0, escala, 0, 0);

    contexto.clearRect(0, 0, largura, altura);

    // Não desenha quando não existem medições.
    if (!historicoGas || historicoGas.length === 0) {
        return;
    }

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
    const pontos = historicoGas.map((leitura, indice) => {
        const valor = Math.max(
            0,
            Math.min(Number(leitura.gas_percentual) || 0, 100)
        );

        const x = historicoGas.length === 1
            ? margem.esquerda + larguraGrafico / 2
            : margem.esquerda + (
                indice / (historicoGas.length - 1)
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

    // Linhas horizontais e valores do eixo vertical.
    contexto.font = "12px Arial";
    contexto.textAlign = "right";
    contexto.textBaseline = "middle";

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
        contexto.fillText(`${valor}%`, margem.esquerda - 10, y);
    }

    // Gradiente abaixo da linha.
    const gradiente = contexto.createLinearGradient(
        0,
        margem.superior,
        0,
        margem.superior + alturaGrafico
    );

    gradiente.addColorStop(0, "rgba(14, 165, 200, 0.25)");
    gradiente.addColorStop(1, "rgba(14, 165, 200, 0.01)");

    // Área preenchida.
    if (pontos.length > 1) {
        contexto.beginPath();

        contexto.moveTo(
            pontos[0].x,
            margem.superior + alturaGrafico
        );

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

    // Linha principal.
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

    // Pontos das medições.
    pontos.forEach(ponto => {
        contexto.beginPath();
        contexto.arc(ponto.x, ponto.y, 4, 0, Math.PI * 2);

        contexto.fillStyle = "#0ea5c8";
        contexto.fill();

        contexto.strokeStyle = "#0d1520";
        contexto.lineWidth = 2;
        contexto.stroke();
    });

    // Formata data e hora.
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

    // Etiquetas do eixo horizontal.
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

        contexto.fillText(
            formatarData(ponto.data),
            ponto.x,
            margem.superior + alturaGrafico + 15
        );
    }
}


/* =========================================
   3. ATUALIZAÇÃO DOS CARTÕES
   ========================================= */

function atualizarCartoes(dados) {
    const elementos = {
        "total-dispositivos": dados.total_dispositivos,
        "dispositivos-ativos": dados.dispositivos_ativos,
        "dispositivos-inativos": dados.dispositivos_inativos,
        "dispositivos-manutencao": dados.dispositivos_manutencao
    };

    Object.entries(elementos).forEach(([id, valor]) => {
        const elemento = document.getElementById(id);

        if (elemento) {
            elemento.textContent = valor ?? 0;
        }
    });
}


/* =========================================
   4. ATUALIZAÇÃO DOS MEDIDORES
   ========================================= */

function atualizarMedidores(dados) {
    const leitura = dados.ultima_leitura;

    if (!leitura) {
        return;
    }

    animarMedidor(
        "medidor-temperatura",
        leitura.temperatura,
        50,
        " °C"
    );

    animarMedidor(
        "medidor-umidade",
        leitura.umidade,
        100,
        "%"
    );

    animarMedidor(
        "medidor-gas",
        leitura.gas_percentual,
        100,
        "%"
    );
}


/* =========================================
   5. ATUALIZAÇÃO DO GRÁFICO
   ========================================= */

function atualizarGrafico(dados) {
    historicoGas = dados.historico_gas || [];

    const elementoDados = document.getElementById("historico-gas-dados");

    if (elementoDados) {
        elementoDados.textContent = JSON.stringify(historicoGas);
    }

    // Atualiza a mensagem de ausência de leituras.
    const mensagem = document.querySelector(".mensagem-sem-leituras");

    if (mensagem) {
        mensagem.style.display = historicoGas.length === 0
            ? "block"
            : "none";
    }

    desenharGraficoGas();
}


/* =========================================
   6. CONSULTA À API
   ========================================= */

async function buscarDadosDashboard() {
    try {
        const resposta = await fetch("/api/dashboard/", {
            method: "GET",
            headers: {
                "Accept": "application/json"
            },
            credentials: "same-origin"
        });

        if (!resposta.ok) {
            throw new Error(
                `Erro HTTP: ${resposta.status}`
            );
        }

        const dados = await resposta.json();

        // Atualiza os cartões.
        atualizarCartoes(dados);

        // Atualiza os medidores.
        atualizarMedidores(dados);

        // Atualiza o histórico.
        atualizarGrafico(dados);

        console.log("Dashboard atualizado com sucesso.");

    } catch (erro) {
        console.error(
            "Erro ao atualizar a dashboard:",
            erro
        );
    }
}


/* =========================================
   7. INICIALIZAÇÃO DA DASHBOARD
   ========================================= */

document.addEventListener("DOMContentLoaded", function () {

    // Carrega o histórico inicial enviado pelo Django.
    const elementoDados = document.getElementById("historico-gas-dados");

    if (elementoDados) {
        try {
            historicoGas = JSON.parse(elementoDados.textContent);
        } catch (erro) {
            console.error("Erro ao carregar histórico inicial:", erro);
            historicoGas = [];
        }
    }

    // Inicializa os valores atuais dos medidores.
    const temperatura = document.getElementById("medidor-temperatura");
    const umidade = document.getElementById("medidor-umidade");
    const gas = document.getElementById("medidor-gas");

    if (temperatura) {
        temperatura.dataset.valorAtual = 0;

        animarMedidor(
            "medidor-temperatura",
            parseFloat(temperatura.dataset.valor) || 0,
            50,
            " °C"
        );
    }

    if (umidade) {
        umidade.dataset.valorAtual = 0;

        animarMedidor(
            "medidor-umidade",
            parseFloat(umidade.dataset.valor) || 0,
            100,
            "%"
        );
    }

    if (gas) {
        gas.dataset.valorAtual = 0;

        animarMedidor(
            "medidor-gas",
            parseFloat(gas.dataset.valor) || 0,
            100,
            "%"
        );
    }

    // Desenha o histórico inicial.
    desenharGraficoGas();

    // Busca os dados imediatamente ao abrir a dashboard.
    buscarDadosDashboard();

    // Atualiza automaticamente a cada 5 segundos.
    setInterval(buscarDadosDashboard, 5000);

    // Redesenha o gráfico quando a janela mudar de tamanho.
    window.addEventListener("resize", desenharGraficoGas);
});
