from flask import Flask, render_template, url_for, redirect, abort, request, session, flash
from repository import SQLiteProdutoRepository
from entidades import Produto
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave"

repo = SQLiteProdutoRepository()

# ----------------- Carrinho (sessão) -----------------
def _get_cart() -> dict:
    cart = session.get("cart")
    if not cart:
        cart = {}
        session["cart"] = cart
    return cart

def _cart_count() -> int:
    return sum(int(q) for q in _get_cart().values())

def _cart_items():
    itens = []
    for pid_str, qtd in _get_cart().items():
        try:
            prod = repo.buscar_produto(int(pid_str))
            if prod:
                itens.append({"produto": prod, "quantidade": int(qtd)})
        except Exception:
            continue
    return itens

@app.context_processor
def inject_cart_info():
    return {"cart_count": _cart_count()}

# ----------------- Catálogo -----------------
@app.route("/")
def homepage():
    produtos = repo.listar_produtos()
    return render_template("index.html", produtos=produtos)

@app.route("/produto/<int:product_id>")
def produto_detalhe(product_id: int):
    produto = repo.buscar_produto(product_id)
    if not produto:
        abort(404, "Produto não encontrado")
    return render_template("produto.html", produto=produto)

# ----------------- Carrinho -----------------
@app.route("/carrinho")
def ver_carrinho():
    itens = _cart_items()
    frete = 15.0
    return render_template("carrinho.html", itens=itens, frete=frete)

@app.route("/adicionar/<int:product_id>", methods=["POST"])
def adicionar_ao_carrinho(product_id: int):
    produto = repo.buscar_produto(product_id)
    if not produto:
        abort(404, "Produto não encontrado")

    try:
        qtd = max(1, int(request.form.get("quantidade", "1")))
    except ValueError:
        qtd = 1

    cart = _get_cart()
    atual = int(cart.get(str(product_id), 0))
    novo = atual + qtd
    if produto.quantidade and novo > produto.quantidade:
        novo = produto.quantidade
        flash("Quantidade ajustada ao estoque disponível.", "warning")

    cart[str(product_id)] = novo
    session["cart"] = cart
    return redirect(url_for("ver_carrinho"))

@app.route("/atualizar-carrinho/<int:product_id>", methods=["POST"])
def atualizar_carrinho(product_id: int):
    produto = repo.buscar_produto(product_id)
    if not produto:
        abort(404, "Produto não encontrado")

    cart = _get_cart()
    atual = int(cart.get(str(product_id), 0))
    delta = request.form.get("delta")
    if delta in ("-1", "1"):
        alvo = atual + int(delta)
    else:
        try:
            alvo = int(request.form.get("quantidade", atual))
        except ValueError:
            alvo = atual

    alvo = max(1, alvo)
    if produto.quantidade:
        alvo = min(alvo, produto.quantidade)

    cart[str(product_id)] = alvo
    session["cart"] = cart
    return redirect(url_for("ver_carrinho"))

@app.route("/remover/<int:product_id>", methods=["POST"])
def remover_do_carrinho(product_id: int):
    cart = _get_cart()
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("ver_carrinho"))

# ----------------- Checkout / Confirmação -----------------
def _calc_totais(itens, frete=0.0):
    subtotal = sum(i["produto"].preco * i["quantidade"] for i in itens)
    return subtotal, subtotal + frete


@app.route("/finalizar", methods=["POST"])
def finalizar_compra():
    return redirect(url_for("checkout"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    itens = _cart_items()
    if not itens:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("ver_carrinho"))

    frete = 15.0
    subtotal, total = _calc_totais(itens, frete)

    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
            "cep": request.form.get("cep", "").strip(),
            "endereco": request.form.get("endereco", "").strip(),
            "cidade": request.form.get("cidade", "").strip(),
            "uf": request.form.get("uf", "").strip().upper(),
            "numero": request.form.get("numero", "").strip(),
            "complemento": request.form.get("complemento", "").strip(),
            "bairro": request.form.get("bairro", "").strip(),
            "telefone": request.form.get("telefone", "").strip(),
            "cpf": request.form.get("cpf", "").strip(),
            "pagamento": request.form.get("pagamento", "pix"),
            "observacoes": request.form.get("observacoes", "").strip(),
        }
        erros = []
        if not dados["nome"]: erros.append("Informe seu nome completo.")
        if not dados["email"]: erros.append("Informe um e-mail válido.")
        if not dados["cep"] or not dados["endereco"] or not dados["cidade"] or not dados["uf"]:
            erros.append("Complete CEP, Endereço, Cidade e UF.")

        if erros:
            for e in erros: flash(e, "danger")
            return render_template("checkout.html", itens=itens, frete=frete, subtotal=subtotal, total=total, dados=dados)

        codigo = "NA-" + datetime.now().strftime("%Y%m%d%H%M%S")
        pedido = {
            "codigo": codigo,
            "itens": [{"id": i["produto"].id, "nome": i["produto"].nome, "preco": i["produto"].preco, "qtd": i["quantidade"]} for i in itens],
            "frete": frete, "subtotal": subtotal, "total": total, "dados": dados,
        }
        session["last_order"] = pedido
        session["cart"] = {}  # limpa carrinho
        return redirect(url_for("confirmacao", codigo=codigo))

    return render_template("checkout.html", itens=itens, frete=frete, subtotal=subtotal, total=total, dados={})

@app.route("/confirmacao/<codigo>")
def confirmacao(codigo):
    pedido = session.get("last_order")
    if not pedido or pedido.get("codigo") != codigo:
        flash("Não encontramos esse pedido na sua sessão.", "warning")
        return redirect(url_for("homepage"))
    return render_template("confirmacao.html", pedido=pedido)



if __name__ == "__main__":
    app.run(debug=True)
