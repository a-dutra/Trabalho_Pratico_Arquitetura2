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
    def __init__(self, tag= None, dados= None, estado= Estado.INVALID):
        self.tag= tag
        self.dados= dados
        self.estado= estado

    def __str__(self):
        return  str(self.dados) + ' | Bloco: ' + str(self.tag) + ' | Estado: '+ self.estado.value

class MemoriaCache:
    def __init__(self, tamanho, tamanho_linha,sistema):
        self.tamanho= tamanho
        self.tamanho_linha= tamanho_linha #Quantos endereços da RAM cabem dentro de uma linha da cache
        

linha = Linha()
linha.tag=2
linha.dados= [2,3,4]
linha.estado= Estado.EXCLUSIVE
print(linha)
