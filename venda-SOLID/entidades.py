class Produto:
    def __init__(self, id, nome, preco, quantidade=0):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

class CarrinhoDeCompras:
    def __init__(self, repositorio):
        self.produtos_no_carrinho = {} 
        self.repositorio = repositorio

    def adicionar_produto(self, produto, quantidade=1):
        produto_em_estoque = self.repositorio.buscar_produto(produto.id)
        
    
        if produto_em_estoque and produto_em_estoque.quantidade >= quantidade:
            if produto.id in self.produtos_no_carrinho:
                self.produtos_no_carrinho[produto.id] += quantidade
            else:
                self.produtos_no_carrinho[produto.id] = quantidade
      
            print(f"Adicionado {quantidade}x '{produto.nome}' ao carrinho.")
        else:
            raise ValueError("Estoque insuficiente para o produto: " + produto.nome)

    def calcular_total(self):
        total = 0
        for id_produto, quantidade in self.produtos_no_carrinho.items():
            produto = self.repositorio.buscar_produto(id_produto)
            if produto:
               
                total += produto.preco * quantidade
        return total
