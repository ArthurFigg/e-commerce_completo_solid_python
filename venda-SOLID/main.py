from entidades import  CarrinhoDeCompras
from descontos import RegraDeDescontoFixo, RegraDeDescontoPercentual, RegraDeDesconto
from pagamentos import Pagavel, Estornavel, PagamentoCartao, PagamentoPIX
from estoque import  Produto
from processador import ProcessadorDePedidos
from repository import SQLiteProdutoRepository, criar_banco

def main():
    criar_banco()
    
    meu_repositorio = SQLiteProdutoRepository()
    
    produto1 = Produto(1, "arroz", 50.0, quantidade=1)
    produto2 = Produto(2, "biscoito", 75.0, quantidade=20)

    meu_repositorio.adicionar_produto(produto1)
    meu_repositorio.adicionar_produto(produto2)

    carrinho = CarrinhoDeCompras(meu_repositorio)
    carrinho.adicionar_produto(produto1, 1)  
    carrinho.adicionar_produto(produto2, 1)  
    
    regras_de_desconto = [
        RegraDeDescontoFixo(20),  
        RegraDeDescontoPercentual(10)  
    ]
    
    metodo_pagamento = PagamentoCartao() 
    
    processador = ProcessadorDePedidos(carrinho, regras_de_desconto, metodo_pagamento, meu_repositorio)

    processador.processar_pedido()

if __name__ == "__main__":
    main()