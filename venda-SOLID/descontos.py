from abc import ABC, abstractmethod


class RegraDeDesconto(ABC):
    @abstractmethod
    def calcular_desconto(self, carrinho):
        pass

class RegraDeDescontoFixo(RegraDeDesconto):
    def __init__(self, valor_fixo):
        self.valor_fixo = valor_fixo

    def calcular_desconto(self, carrinho):
        return self.valor_fixo

class RegraDeDescontoPercentual(RegraDeDesconto):
    def __init__(self, percentual):
        self.percentual = percentual

    def calcular_desconto(self, carrinho):
        total = carrinho.calcular_total()
        if total > 100:
            return total * (self.percentual / 100)
        return 0
