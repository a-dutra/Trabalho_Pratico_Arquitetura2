from sistema import Sistema

# Configurações gerais do sistema
TAMANHO_MEMORIA = 50         # número total de endereços da RAM
TAMANHO_BLOCO = 5            # quantidade de endereços por bloco
TAMANHO_CACHE = 10           # capacidade total da cache
TAMANHO_LINHA_CACHE = 5      # tamanho de um bloco dentro da cache
QUANTIDADE_PROCESSADORES = 3 # número de estações climáticas (processadores)

def main():
    # Inicializa o sistema completo
    sistema = Sistema(
        qntd_processadores=QUANTIDADE_PROCESSADORES,
        tamanho_cache=TAMANHO_CACHE,
        tamanho_linha_cache=TAMANHO_LINHA_CACHE,
        tamanho_memoria=TAMANHO_MEMORIA,
        tamanho_bloco=TAMANHO_BLOCO
    )

    # Executa o sistema (menu principal)
    sistema.executar()


if __name__ == "__main__":
    main()