from enum import Enum

#Estados possíveis de uma linha na cache
class Estado(Enum):
    M = "Modified"    #sera que aq nao é melhor colocar so as letras
    E = "Exclusive"
    S = "Shared"
    I = "Invalid"
    F = "Forward"

class Resposta:
    HIT = 1
    MISS = 2   

class Linha:
    def __init__(self, tag= None, dados= None, estado= Estado.I):
        self.tag= tag
        self.dados= dados
        self.estado= estado

    def __str__(self):
        return  str(self.dados) + ' | Bloco: ' + str(self.tag) + ' | Estado: '+ self.estado.value

class MemoriaCache:
    def __init__(self, tamanho, tamanho_linha,sistema):
        self.tamanho= tamanho
        self.tamanho_linha= tamanho_linha #Quantos endereços da RAM cabem dentro de uma linha da cache
        self.sistema= sistema
        self.qntd_linhas= tamanho//tamanho_linha
        self.memoria= [Linha() for _ in range(self.qntd_linhas)]
        self.fila= []

    def __str__(self):
        buffer = ''
        for i in range(self.qntd_linhas):
            buffer += f'\033[34mLinha {i}:\033[00m {self.memoria[i]}\n'
        return buffer

    def procurar_linha(self,endereco):
        '''Procura a linha que armazena o *endereco* na cache, retornando a linha se encontrada.
        Caso a linha não seja encontrada, ou seja inválida, retorna None.
        '''
        tag= endereco//self.tamanho_linha #calcula número do bloco
        for i in range(self.qntd_linhas):
            if self.memoria[i].tag==tag and self.memoria[i].estado !=Estado.I:
                return self.memoria[i] #HIT (retorna informações da linha)
            return None

    def ler(self, endereco):
        '''Lê o dado no *endereço* da memória principal e se encontrar, retorna HIT.
        Caso a cache não possua a linha que armazena o *endereço*, retorna MISS.
        '''
        #Procura linha dentro da cache
        linha=self.procurar_linha(endereco)

        #Qual indice corresponde ao endereço acessado
        indice= endereco % self.tamanho_linha
        if linha is not None and linha.estado != Estado.I:
            return linha.dados[indice], Resposta.HIT
        return None, Resposta.MISS
    
    def carregar_linha(bloco,endereco,estado):
        pass

    def atualizar_linha(endereco,dado):
        pass

    def invalidar_linha(endereco):
        pass

    def shared_para_forward():
        pass
