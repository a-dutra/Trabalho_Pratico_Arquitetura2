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

    def executar(self):
        '''Funcao necessária para a interação com o usuário, mostra as opções de escolha '''

        print(f"Processador {self.id} executando...")
        while True:
            print("\n>>> Escolha a operação:")
            print("1: Ler")
            print("2: Escrever")
            print("c: Mostrar cache")
            print("m: Mostrar memória principal")
            print("v: Voltar")

            escolha = input("\n> ").strip()
            #volta
            if escolha == 'v':
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
                    tipo, valor = self.ler(endereco)  # desempacota a tupla retornada
                    print(f"\nValor em [{endereco:03}] = ({tipo.name}, {valor:.2f})")


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

                try:
                    # tenta converter para inteiro
                    tipo_int = int(dado)

                    # verifica se o valor existe no enum
                    if tipo_int not in [t.value for t in TipoSensor]:
                        raise ValueError

                    tipo = TipoSensor(tipo_int)

                except:
                    print("Tipo inválido.")
                    continue

                # inserir valor que vai ser armazenado no sensor 
                val_input = input("Valor (número): ").strip()
                try: #se nao conseguir converter para float da erro
                    valor = float(val_input)
                except:
                    print("Valor inválido.")
                    continue

                dado = (tipo, valor) #constroi a tupla
                self.escrever(endereco, dado)
                print(f"Escrito em [{endereco:03}] = ({dado[0].name}, {dado[1]:.2f})")
                    
            else:
                print("Opção inválida.")

    def ler(self, endereco: int):
        '''le um dado no *endereço* da memória'''

        resposta = self.cache.ler(endereco) #chama o metodo ler da cache local
        if resposta[1] == Resposta.HIT: #se a cache tem o dado
            print("Read Hit")
            return resposta[0] #retorna o valor
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
                            # write-back antes de transferir 
                            endereco_sub = linha.tag * self.cache.tamanho_linha 
                            self.memoria_principal.atualizar_bloco(linha.dados, endereco_sub) 
                            linha.estado = Estado.F
                            self.cache.carregar_linha(linha.dados, endereco, Estado.S)
                        return cache.ler(endereco)[0]
        
            # Se não achou em caches
            print("Buscando na memória principal...")
            bloco = self.memoria_principal.buscar_bloco(endereco)  # procura o bloco inteiro na RAM
            self.cache.carregar_linha(bloco, endereco, Estado.E)  # carrega o valor com estado E
            tipo, valor = self.memoria_principal.ler(endereco)
            return tipo, valor
        
    def escrever(self, endereco: int, dado: Tuple[TipoSensor, float]):
        '''Escreve um *dado* no endereço da memória'''

        linha = self.cache.procurar_linha(endereco)
        if linha is not None:
            print("Write Hit")
            offset = endereco % self.cache.tamanho_linha #determinar qual linha escrever
            if linha.estado == Estado.M: #o bloco esta na cache e já foi modificado
                linha.dados[offset] = dado
            elif linha.estado == Estado.E: #o bloco está na cache e é exclusivo
                linha.dados[offset] = dado
                linha.estado = Estado.M #muda o estado 
            elif linha.estado == Estado.F or linha.estado == Estado.S: #bloco é compartilhado
                # invalidar outras caches
                for cache in self.sistema.caches:
                    if cache != self.cache:
                        if cache.procurar_linha(endereco) is not None:
                            cache.invalidar_linha(endereco)
                linha.dados[offset] = dado
                linha.estado = Estado.M
        else:
            print("Write Miss")
            #procura em outras caches
            for cache in self.sistema.caches:
                if cache != self.cache:
                    resposta = cache.procurar_linha(endereco)
                    if resposta is not None:
                        print("Bloco encontrado em outra cache.")
                        if resposta.estado == Estado.F or resposta.estado == Estado.S or resposta.estado == Estado.E :
                            #invalidar todas
                            for cache in self.sistema.caches:
                                if cache != self.cache:
                                    if cache.procurar_linha(endereco) is not None:
                                        cache.invalidar_linha(endereco)
                            self.cache.carregar_linha(resposta.dados, endereco, Estado.M) #se existe esse dado em outras caches devemos mudar o estado do dado para M
                            #escreve o novo valor na linha 
                            linha_local = self.cache.procurar_linha(endereco) 
                            linha_local.dados[endereco % self.cache.tamanho_linha] = dado
                            return
                        elif resposta.estado == Estado.M:
                            #write-back
                            endereco_sub = resposta.tag * self.cache.tamanho_linha
                            self.memoria_principal.atualizar_bloco(resposta.dados, endereco_sub) #atualiza a RAM com a versao mais recente do bloco
                            resposta.estado = Estado.I #invalidar a linha da outra cache
                            break
            #se não encontrou em caches, busca na RAM e carrega como M
            print("Buscando bloco na memória principal...")
            self.cache.carregar_linha(self.memoria_principal.buscar_bloco(endereco), endereco, Estado.M)
            linha_local = self.cache.procurar_linha(endereco)
            linha_local.dados[endereco % self.cache.tamanho_linha] = dado # escrita do dado dentro do bloco da cache
