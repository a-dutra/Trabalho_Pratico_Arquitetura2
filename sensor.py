from enum import Enum
import random

# Tipos de dados que podem existir na memória principal
class TipoSensor(Enum):
    TEMPERATURA = 0
    UMIDADE = 1
    PRESSAO = 2
    VENTO = 3
    UV = 4

class SensorClimatico:
    def __init__(self, tipo: TipoSensor):
        self.tipo = tipo

    def gerar_valor(self):
        '''Gera valores realistas para cada tipo de sensor'''

        if self.tipo == TipoSensor.TEMPERATURA:
            return random.uniform(-10, 40)  # °C
        elif self.tipo == TipoSensor.UMIDADE:
            return random.uniform(0, 100)   # %
        elif self.tipo == TipoSensor.PRESSAO:
            return random.uniform(950, 1050)  # hPa
        elif self.tipo == TipoSensor.VENTO:
            return random.uniform(0, 120)   # km/h
        elif self.tipo == TipoSensor.UV:
            return random.uniform(0, 12)    # índice UV


def gerar_valor_aleatorio(tipo: TipoSensor):
    '''Função para criar um valor aleatório para um tipo específico'''
    sensor = SensorClimatico(tipo)
    return sensor.gerar_valor()

def gerar_memoria_inicial(qtd_posicoes):
    '''Gera uma lista completa de valores iniciais para a memória principal'''

    tipos = list(TipoSensor)
    memoria = []

    for i in range(qtd_posicoes):
        tipo = random.choice(tipos)      # sorteia qual dado será colocado naquela posição
        valor = gerar_valor_aleatorio(tipo)
        memoria.append((tipo, valor))    # guarda uma tupla: (tipo, valor)

    return memoria

print("Temperatura:", SensorClimatico(TipoSensor.TEMPERATURA).gerar_valor())
print("Umidade:", SensorClimatico(TipoSensor.UMIDADE).gerar_valor())
print("Pressão:", SensorClimatico(TipoSensor.PRESSAO).gerar_valor())
print(gerar_valor_aleatorio(TipoSensor.VENTO))
print(gerar_valor_aleatorio(TipoSensor.UV))
