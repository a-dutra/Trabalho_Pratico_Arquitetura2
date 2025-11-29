from sistema import Sistema

# Configurações gerais do sistema
TAMANHO_MEMORIA = 50        
TAMANHO_BLOCO = 5        
TAMANHO_CACHE = 10           
TAMANHO_LINHA_CACHE = 5      
QUANTIDADE_PROCESSADORES = 3 

def main():
    # inicializa o sistema completo
    sistema = Sistema(
        qntd_processadores=QUANTIDADE_PROCESSADORES,
        tamanho_cache=TAMANHO_CACHE,
        tamanho_linha_cache=TAMANHO_LINHA_CACHE,
        tamanho_memoria=TAMANHO_MEMORIA,
        tamanho_bloco=TAMANHO_BLOCO
    )

    sistema.executar()


if __name__ == "__main__":
    main()