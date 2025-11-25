from enum import Enum

class Estado(Enum):
    MODIFIED = "Modified"
    EXCLUSIVE = "Exclusive"
    SHARED = "Shared"
    INVALID = "Invalid"
    FORWARD = "Forward"

class Resposta:
    HIT = 1
    MISS = 2   

class Linha:
    def __init__(self, tag, dados, estado):
        self.tag= None
        self.dados=None
        self.estado= Estado.INVALID 

class MemoriaCache:
    def __init__(self, tamanho, tamanho_linha,sistema):
        self.tamanho= tamanho
        self.tamanho_linha= tamanho_linha #Quantos endereços da RAM cabem dentro de uma linha da cache
