from abc import ABC, abstractmethod


class Pagavel(ABC):
    @abstractmethod
    def pagar(self, valor):
        pass

class Estornavel(ABC):
    @abstractmethod
    def estornar(self, valor):
        pass

class PagamentoCartao(Pagavel, Estornavel):
    def pagar(self, valor):
        print(f"Pagamento de R${valor:.2f} realizado com cartão.")

    def estornar(self, valor):
        print(f"Estorno de R${valor:.2f} realizado no cartão.")

class PagamentoPIX(Pagavel):
    def pagar(self, valor):
        print(f"Pagamento de R${valor:.2f} realizado via PIX.")