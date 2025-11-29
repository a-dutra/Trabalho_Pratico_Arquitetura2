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
        '''Inicializa o sensor'''
        self.tipo = tipo

    def gerar_valor(self):
        '''Gera valores realistas para cada tipo de sensor'''

        if self.tipo == TipoSensor.TEMPERATURA:
            return round(random.uniform(-10, 40),1)  # °C
        elif self.tipo == TipoSensor.UMIDADE:
            return round(random.uniform(0, 100),1)   # %
        elif self.tipo == TipoSensor.PRESSAO:
            return round(random.uniform(950, 1050),2)  # hPa
        elif self.tipo == TipoSensor.VENTO:
            return round(random.uniform(0, 120),2)   # km/h
        elif self.tipo == TipoSensor.UV:
            return round(random.uniform(0, 12),2)    # índice UV


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

