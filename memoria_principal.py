from sensor import TipoSensor, gerar_memoria_inicial

class MemoriaPrincipal:
    def __init__(self, tamanho: int, tamanho_bloco: int):
        self.tamanho = tamanho
        self.tamanho_bloco = tamanho_bloco

        #A RAM já começa preenchida com dados aleatórios
        self.memoria = gerar_memoria_inicial(tamanho)

    def __str__(self):
        buffer = "===== MEMÓRIA PRINCIPAL =====\n"
        for i, (tipo, valor) in enumerate(self.memoria):
            buffer += f"[{i:03}] {tipo.name:<12} {valor:.2f}\n"
        return buffer


    def ler(self, endereco: int):
        """Retorna o dado no endereço da memória."""
        if endereco >= self.tamanho:
            raise ValueError(f"Endereço {endereco} fora do limite ({self.tamanho}).")
        return self.memoria[endereco]

    def escrever(self, endereco: int, dado):
        """Escreve um dado no endereço da memória."""
        if endereco >= self.tamanho:
            raise ValueError(f"Endereço {endereco} fora do limite ({self.tamanho}).")
        self.memoria[endereco] = dado #dado é uma tupla (TipoSensor, valor). É o que eu quero escrever na RAM


    def buscar_bloco(self, endereco: int):
        """Retorna o bloco inteiro do endereço pedido."""
        inicio = (endereco // self.tamanho_bloco) * self.tamanho_bloco
        fim = inicio + self.tamanho_bloco
        return self.memoria[inicio:fim]

    def atualizar_bloco(self, bloco, endereco: int):
        """Sobrescreve o bloco da RAM que contém o endereço."""

        #Também usado quando a cache quer escrever de volta na RAM (write-back):
        inicio = (endereco // self.tamanho_bloco) * self.tamanho_bloco
        fim = inicio + self.tamanho_bloco
        self.memoria[inicio:fim] = bloco
