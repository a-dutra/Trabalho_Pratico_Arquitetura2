from memoria_principal import MemoriaPrincipal
from memoria_cache import MemoriaCache
from processador import Processador

class Sistema:
    def __init__(self, qntd_processadores, tamanho_cache, tamanho_linha_cache,tamanho_memoria, tamanho_bloco):
        self.memoria_principal= MemoriaPrincipal (tamanho_memoria, tamanho_bloco)
        self.caches= [MemoriaCache(tamanho_cache, tamanho_linha_cache, self)
            for _ in range(qntd_processadores)]
        self.processadores = []
        for i in range(qntd_processadores):
            cache_atual = self.caches[i]
            processador = Processador(i + 1,cache_atual, self.memoria_principal,self)
            self.processadores.append(processador)

    def executar(self):
        print("\n ===== SIMULADOR DE UM SISTEMA DISTRIBUÍDO DE MONITORAMENTO CLIMÁTICO =====\n")

        while True:
            print("Selecione uma estação climática para acessar:\n")

            for i in range(1, len(self.processadores) + 1):
                print(f"{i}: Estação {i}")

            print("m: Ver dados climáticos armazenados")
            print("q: Sair")

            escolha = input("\n> ")

            # Sair
            if escolha == 'q':
                print("Sistema finalizado.")
                return

            # Mostrar memória
            elif escolha == 'm':
                print("Memória principal:\n")
                print(self.memoria_principal)

            # Verificar se é número
            elif escolha != "" and all('0' <= c <= '9' for c in escolha):
                processador_id = int(escolha) - 1

                if 0 <= processador_id < len(self.processadores):
                    self.processadores[processador_id].executar()
                else:
                    print("\nOpção Inválida.")

            # Qualquer outra coisa é inválida
            else:
                print("\nOpção Inválida.")
