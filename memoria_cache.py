from enum import Enum

#Estados possíveis de uma linha na cache
class Estado(Enum):
    M = "Modified"   
    E = "Exclusive"
    S = "Shared"
    I = "Invalid"
    F = "Forward"

class Resposta:
    HIT = 1
    MISS = 2   

class Linha:

    def __init__(self, tag= None, dados= None, estado= Estado.I):
        '''Cria uma linha de cache, armazenando a tag do bloco, seus dados e o estado no protocolo de coerência'''
        self.tag= tag
        self.dados= dados
        self.estado= estado

    def __str__(self):
        '''Retorna em forma de texto as linhas da cache, mostrando os dados, a tag do bloco e o estado atual'''
        if self.dados is None:
            dados_str = "None"
        else:
            dados_str = ""
            for i, item in enumerate(self.dados):
                if item is None:
                    dados_str += "None"
                else:
                    tipo, valor = item
                    dados_str += f"({tipo.name}, {valor})"
                if i < len(self.dados) - 1:
                    dados_str += ", "
        return f"{dados_str} | Bloco: {self.tag} | Estado: {self.estado.value}"

class MemoriaCache:
    def __init__(self, tamanho, tamanho_linha,sistema):
        '''Inicializa a cache definindo seu tamanho, o tamanho de cada linha e a referência ao sistema de coerência'''
        self.tamanho= tamanho
        self.tamanho_linha= tamanho_linha #Quantos endereços da RAM cabem dentro de uma linha da cache
        self.sistema= sistema
        self.qntd_linhas= tamanho//tamanho_linha
        self.memoria= [Linha() for _ in range(self.qntd_linhas)]
        self.fila= []

    def __str__(self):
        '''Retorna em forma de texto todas aas linhas da cache'''
        buffer = ''
        for i in range(self.qntd_linhas):
            buffer += f'Linha {i}:{self.memoria[i]}\n'
        return buffer

    def procurar_linha(self,endereco):
        '''Procura a linha que armazena o *endereco* na cache, retornando a linha se encontrada. 
        Caso a linha não seja encontrada, ou seja inválida, retorna None'''
        tag= endereco//self.tamanho_linha #define em qual bloco esta armazenado o endereco
        for i in range(self.qntd_linhas):
            if self.memoria[i].tag==tag and self.memoria[i].estado !=Estado.I:
                return self.memoria[i] #HIT (retorna informações da linha)
        return None

    def ler(self, endereco):
        '''Lê o dado no *endereço* da memória principal e se encontrar, retorna HIT.
        Caso a cache não possua a linha que armazena o *endereço*, retorna MISS'''

        linha=self.procurar_linha(endereco)

        #Qual indice corresponde ao endereço acessado
        indice= endereco % self.tamanho_linha
        if linha is not None and linha.estado != Estado.I:
            return linha.dados[indice], Resposta.HIT
        return None, Resposta.MISS
    
    def carregar_linha(self, bloco, endereco: int, estado: Estado):
        '''Carrega um bloco da memória principal para a cache. Esta função é utilizada quando ocorre um MISS. Ela insere o bloco
        solicitado em alguma linha da cache'''

        tag = endereco // self.tamanho_linha   
        for i in range (self.qntd_linhas):
            if self.memoria[i].estado == Estado.I: 
                self.memoria[i].tag = tag
                self.memoria[i].dados = bloco.copy()
                self.memoria[i].estado = estado
                self.fila.append(i)
                return
        # se a cache estiver cheia, aplica a política de substituição FIFO
        index_removido = self.fila.pop(0)

        # se a linha a ser substituída estiver no estado M, atualiza o bloco na memória principal
        if self.memoria[index_removido].estado == Estado.M:
            endereco_substituido = self.memoria[index_removido].tag * self.tamanho_linha
            self.sistema.memoria_principal.atualizar_bloco(self.memoria[index_removido].dados, endereco_substituido)
        # se a linha a ser substituída estiver em F, outra cache no estado S, irá para F
        elif self.memoria[index_removido].estado == Estado.F:
            self.shared_para_forward(self.memoria[index_removido].tag)
        self.memoria[index_removido].tag = tag
        self.memoria[index_removido].dados = bloco
        self.memoria[index_removido].estado = estado
        self.fila.append(index_removido)


    def atualizar_linha(self,endereco,dado):
        '''Atualiza o valor da linha com o novo valor *dado*'''

        tag = endereco // self.tamanho_linha  
        for i in range (self.qntd_linhas):
            if self.memoria[i].tag == tag:
                self.memoria[i].dados[endereco % self.tamanho_linha] = dado # encontra o bof que define a posicao onde o novo dado vai ser inserido e atualiza
                return


    def invalidar_linha(self, endereco:int ):
        '''Invalida a linha que contém o *enderço* solicitado pelo processador, e tira a linha da fila'''

        tag = endereco // self.tamanho_linha  
        for i in range (self.qntd_linhas):
            if self.memoria[i].tag == tag:
                self.memoria[i].estado = Estado.I 
                if i in self.fila:
                    self.fila.remove(i) 
                return 

    def shared_para_forward(self, tag: int):
        '''Transforma uma linha S para F (a primeria que encontrar), em outra cache que compartilha a mesma linha '''

        for cache in self.sistema.caches:
            if cache != self:
                for linha in cache.memoria:
                    if linha.tag == tag and linha.estado == Estado.S:
                        linha.estado = Estado.F
                        return
