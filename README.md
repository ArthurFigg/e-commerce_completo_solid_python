# E-commerce com Princípios SOLID em Python

Sistema de e-commerce desenvolvido em Python com Flask, aplicando os princípios
SOLID de design orientado a objetos. Projeto desenvolvido como estudo prático
de arquitetura de software.

## Sobre o projeto

O objetivo foi construir um sistema de vendas funcional usando boas práticas
de programação orientada a objetos. Cada camada do sistema foi pensada para
ter responsabilidade única, ser extensível e depender de abstrações.

## Tecnologias

- Python 3.13
- Flask
- SQLite
- Bootstrap 5
- Jinja2

## Funcionalidades

- Catálogo de produtos com página de detalhe
- Carrinho de compras persistido em sessão
- Controle de estoque com validação de quantidade
- Checkout com formulário e validação de dados
- Suporte a múltiplos métodos de pagamento (Cartão e PIX)
- Página de confirmação de pedido

## Como rodar

```bash
# Clone o repositório
git clone https://github.com/ArthurFigg/e-commerce_completo_solid_python.git
cd e-commerce_completo_solid_python/venda-SOLID

# Instale as dependências
pip install flask

# Rode a aplicação
python estoque.py
```

Acesse em: http://localhost:5000

## Princípios SOLID aplicados

**S — Single Responsibility:** cada classe tem uma responsabilidade única.
`SQLiteProdutoRepository` cuida só do banco, `CarrinhoDeCompras` só do carrinho,
`ProcessadorDePedidos` só do processamento do pedido.

**O — Open/Closed:** novos tipos de desconto podem ser adicionados criando uma
nova classe, sem modificar o código existente. Exemplo: `RegraDeDescontoFixo`
e `RegraDeDescontoPercentual`.

**I — Interface Segregation:** `Pagavel` e `Estornavel` são interfaces separadas.
`PagamentoPIX` implementa só `Pagavel`, pois PIX não tem estorno.
`PagamentoCartao` implementa as duas.

**D — Dependency Inversion:** `ProcessadorDePedidos` recebe o método de pagamento
como parâmetro, dependendo da abstração `Pagavel`, não de uma implementação
específica.

## Aprendizados

Aplicar SOLID num projeto real mostrou como a separação de responsabilidades
torna o código mais fácil de estender. Adicionar um novo método de pagamento
ou uma nova regra de desconto não exige mexer no que já funciona.
