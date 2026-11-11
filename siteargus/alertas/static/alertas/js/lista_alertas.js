document.addEventListener('DOMContentLoaded', () => {

    // Intervalo de atualização: 5 segundos.
    const INTERVALO_ATUALIZACAO = 5000;

    const statusAtualizacao = document.getElementById(
        'status-atualizacao'
    );

    // Atualiza a página somente quando ela estiver visível.
    setInterval(() => {

        if (document.visibilityState === 'visible') {

            if (statusAtualizacao) {
                statusAtualizacao.textContent =
                    'Atualizando alertas...';
            }

            window.location.reload();
        }

    }, INTERVALO_ATUALIZACAO);

});