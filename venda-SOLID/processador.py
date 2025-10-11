from estoque import Produto

class ProcessadorDePedidos:
    def __init__(self, carrinho, lista_de_regras, processador_pagamento, repositorio):
        self.carrinho = carrinho
        self.lista_de_regras = lista_de_regras
        self.processador_pagamento = processador_pagamento
        self.repositorio = repositorio

    def processar_pedido(self):
        if not self.carrinho.produtos_no_carrinho:
            print("O carrinho está vazio. Adicione itens para processar o pedido.")
            return
        
        print("--- Iniciando processamento do pedido ---")
        
        total_bruto = self.carrinho.calcular_total()
        
        desconto_total = 0
        for regra in self.lista_de_regras:
            desconto_total += regra.calcular_desconto(self.carrinho)
            
        total_final = max(0, total_bruto - desconto_total)

        print(f"Total Bruto: R${total_bruto:.2f}")
        print(f"Total de Descontos: R${desconto_total:.2f}")
        print(f"Valor a Pagar: R${total_final:.2f}")
        
        print("\nIniciando pagamento...")
        self.processador_pagamento.pagar(total_final)
        
        print("\nAtualizando estoque...")
        for id_produto, quantidade_comprada in self.carrinho.produtos_no_carrinho.items():
            dados_produto = self.repositorio.buscar_produto(id_produto)
            produto_atualizado = Produto(
                id=id_produto,
                nome=dados_produto[1],
                preco=dados_produto[2],
                quantidade=dados_produto[3] - quantidade_comprada
            )
            self.repositorio.atualizar_produto(produto_atualizado)
        
        print("\n--- Pedido Finalizado com Sucesso! ---")