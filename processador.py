from memoria_cache import MemoriaCache, Resposta, Estado
from memoria_principal import MemoriaPrincipal
from sensor import TipoSensor
from typing import Tuple


class Processador:
    def __init__(self, id, cache, memoria_principal, sistema):
        self.id = id
        self.cache = cache #cache particular de cada processador 
        self.memoria_principal = memoria_principal
        self.sistema = sistema #onde contem todas as caches dos outros processadores 


    def imprimir(self):
        '''Funcao necessária para a interação com o usuário, mostra as opções de escolha '''

        print(f"Processador {self.id} executando...")
        while True:
            print("\n>>> Escolha a operação:")
            print("1: Ler")
            print("2: Escrever")
            print("c: Mostrar cache")
            print("m: Mostrar memória principal")
            print("q: Voltar")

            escolha = input("\n> ").strip()
            #volta
            if escolha == 'q':
                print("Processador finalizado.\n")
                return
            #mostra a cache
            elif escolha == 'c':
                print(f"\nCache {self.id}:\n")
                print(self.cache)

            #mostra a memória principal
            elif escolha == 'm':
                print("\nMemória principal:\n")
                print(self.memoria_principal)
            
            #Lê
            elif escolha == '1':
                    endereco = int(input("Endereço: "))
                    print()
                    valor = self.ler(endereco)
                    print(f"\nValor em [{endereco}] = {valor}")

            #escreve
            elif escolha == '2':
                try:
                    endereco = int(input("Endereço: "))
                    if endereco < 0 or endereco >= self.memoria_principal.tamanho:
                        print("Endereço fora dos limites.")
                        continue
                except:
                    print("Endereço inválido.")
                    continue
                # selecionar tipo
                print("Tipos de sensor:")
                for t in TipoSensor:
                    print(f"{t.value}: {t.name}") #mostra as opcoes de sensores disponíveis
                dado = input("Escolha o tipo (número): ").strip() 

                if not dado.isdigit() or int(dado) not in [t.value for t in TipoSensor]: #ver isso aq 
                    print("Tipo inválido.")
                tipo = TipoSensor(int(dado))

                # inserir valor que vai ser armazenado no sensor 
                val_input = input("Valor (número): ").strip()
                try: #se nao conseguir converter para float da erro
                    valor = float(val_input)
                except:
                    print("Valor inválido.")
                    continue

                dado = (tipo, valor) #constroi a tupla
                self.escrever(endereco, dado)
                print(f"Escrito em [{endereco}] = {dado}")
                    
            else:
                print("Opção inválida.")

    def ler(self, endereco: int):
        '''le um dado no *endereço* da memória'''
        resposta = self.cache.ler(endereco) #chama o metodo ler da cahe local
        if resposta[1] == Resposta.HIT: #se a cache tem o dado
            print("Read Hit")
            return resposta[0]
        else: #se a cache local não tem o dado
            print("Read Miss")
            # procura em outras caches
            for cache in self.sistema.caches:
                if cache != self.cache: #diferente da que esta chamando
                    linha = cache.procurar_linha(endereco) 
                    if linha is not None:
                        print("Bloco encontrado em outra cache.")
                        if linha.estado == Estado.F:
                            self.cache.carregar_linha(linha.dados, endereco, Estado.S) #mudança de valores na cache local
                        elif linha.estado == Estado.E:
                            self.cache.carregar_linha(linha.dados, endereco, Estado.S) 
                            linha.estado = Estado.F #cache analisada passa a ser 'F'
                        elif linha.estado == Estado.M: #uma unica cache tem o bloco e foi modificada
                            # write-back antes de transferir (NÁO ENTENDI MTO BEM DESSA PARTE PARA BAIXO)
                            endereco_sub = linha.tag * self.cache.tamanho_linha 
                            self.memoria_principal.atualizar_bloco(linha.dados, endereco_sub) 
                            linha.estado = Estado.F
                            self.cache.carregar_linha(linha.dados, endereco, Estado.S)
                        return cache.ler(endereco)[0]
            # se não achou em caches
            print("Buscando na memória principal...")
            bloco = self.memoria_principal.buscar_bloco(endereco, self.cache.tamanho_linha) #procura o bloco inteiro na RAM
            self.cache.carregar_linha(bloco, endereco, Estado.E) #carrega o valor com estado E pois ninguém mais tem o bloco
            return self.memoria_principal.ler(endereco)
    #CONFERIR ESSE 
    def escrever(self, endereco: int, dado: Tuple[TipoSensor, float]):
        '''Escreve um *dado* no endereço da memória'''
        linha = self.cache.procurar_linha(endereco)
        if linha is not None:
            print("Write Hit")
            offset = endereco % self.cache.tamanho_linha
            if linha.estado == Estado.M:
                linha.dados[offset] = dado
            elif linha.estado == Estado.E:
                linha.dados[offset] = dado
                linha.estado = Estado.M
            elif linha.estado in (Estado.S, Estado.F):
                # invalidar outras caches
                for cache in self.sistema.caches:
                    if cache != self.cache:
                        if cache.procurar_linha(endereco) is not None:
                            cache.invalidar_linha(endereco)
                linha.dados[offset] = dado
                linha.estado = Estado.M
        else:
            print("Write Miss")
            # procura em outras caches
            for cache in self.sistema.caches:
                if cache != self.cache:
                    linha_out = cache.procurar_linha(endereco)
                    if linha_out is not None:
                        print("Bloco encontrado em outra cache.")
                        if linha_out.estado in (Estado.F, Estado.S, Estado.E):
                            # invalidar todas
                            for c in self.sistema.caches:
                                if c != self.cache:
                                    if c.procurar_linha(endereco) is not None:
                                        c.invalidar_linha(endereco)
                            self.cache.carregar_linha(linha_out.dados, endereco, Estado.M)
                            # escreve
                            linha_local = self.cache.procurar_linha(endereco)
                            linha_local.dados[endereco % self.cache.tamanho_linha] = dado
                            return
                        elif linha_out.estado == Estado.M:
                            # write-back
                            endereco_sub = linha_out.tag * self.cache.tamanho_linha
                            self.memoria_principal.atualizar_bloco(linha_out.dados, endereco_sub)
                            linha_out.estado = Estado.I
                            # continue procurar (ou ir pra RAM)
                            break
            # se não encontrou em caches -> buscar na RAM e carregar como MODIFIED
            bloco = self.memoria_principal.buscar_bloco(endereco, self.cache.tamanho_linha)
            self.cache.carregar_linha(bloco, endereco, Estado.M)
            linha_local = self.cache.procurar_linha(endereco)
            linha_local.dados[endereco % self.cache.tamanho_linha] = dado