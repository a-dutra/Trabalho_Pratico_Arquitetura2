class MemoriaPrincipal:
    def __init__(self, tamanho: int, tamanho_bloco: int):
        self.tamanho = tamanho
        self.tamanho_bloco = tamanho_bloco
        self.memoria = [0] * tamanho

    def ler(self, endereco: int):
        '''
        Retorna o dado no *endereço* da memória.
        '''
        if endereco >= self.tamanho:
            raise ValueError(f"Endereço {endereco} fora dos limites da memória.")
        return self.memoria[endereco]
    
    def escrever(self, endereço: int, dado):
        '''
        Escreve o *dado* no *endereço* da memória.
        '''
        if endereço >= self.tamanho:
            raise ValueError(f"Endereço {endereço} fora dos limites da memória.")
        self.memoria[endereço] = dado

    def buscar_bloco(self, endereco: int):
        '''
        Retorna o bloco que contenha o *endereço*.
        '''
        return self.memoria[self.tamanho_bloco * (endereco // self.tamanho_bloco): self.tamanho_bloco * (endereco // self.tamanho_bloco + 1)]
        
    def atualizar_bloco(self, bloco, endereco: int):
        '''
        Atualiza o bloco da memória principal que contém o *endereço*.
        '''
        self.memoria[self.tamanho_bloco * (endereco // self.tamanho_bloco): self.tamanho_bloco * (endereco // self.tamanho_bloco + 1)] = bloco

    def __repr__(self):
        buffer = ''
        for i in range(self.tamanho):
            buffer += '\033[34m{:>3} \033[00m{:<}\n'.format(str(i), str(self.memoria[i]))
        return buffer
