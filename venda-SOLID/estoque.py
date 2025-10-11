class Produto:
    def __init__(self, id, nome, preco, quantidade=0):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

class catalogo: 
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, produto):
        if produto.id in self.produtos:
            raise ValueError("Produto já existe no catalogo.")
        self.produtos[produto.id] = produto

    def remover_produto(self, id):
        if id not in self.produtos:
            raise ValueError("Produto não encontrado no catalogo.")
        del self.produtos[id]

    def buscar_produto(self, id):
        return self.produtos.get(id, None)

    def listar_produtos(self):
        return list(self.produtos.values())

class estoque:
    def __init__(self):
        self.quantidades = {}

    
    def adicionar_estoque(self, id_produto, quantidade):
        if id_produto not in self.quantidades:
            self.quantidades[id_produto] = 0
        self.quantidades[id_produto] += quantidade

  
    def dar_baixa(self, id_produto, quantidade):
        if id_produto not in self.quantidades or self.quantidades[id_produto] < quantidade:
            raise ValueError("Estoque insuficiente.")
        self.quantidades[id_produto] -= quantidade

    
    def verificar_disponibilidade(self, id_produto, quantidade):
        return self.quantidades.get(id_produto, 0) >= quantidade