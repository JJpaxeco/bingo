from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, NumeroSorteado, Cartela, deletar_tudo

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    numeros_sorteados = NumeroSorteado.query.order_by(NumeroSorteado.numero).all()
    proximos_de_vencer = []

    for cartela in Cartela.query.all():
        numeros_cartela = set(cartela.numeros)
        faltando = numeros_cartela - {n.numero for n in numeros_sorteados}
        if len(faltando) <= 3:
            proximos_de_vencer.append((cartela.identificacao, len(faltando)))

    total_proximos = len(proximos_de_vencer)

    return render_template(
        "index.html",
        numeros_sorteados=numeros_sorteados,
        proximos_de_vencer=proximos_de_vencer,
        total_proximos=total_proximos,
    )

@main_bp.route("/adicionar_numero", methods=["POST"])
def adicionar_numero():
    numero = request.form.get("numero")
    if numero:
        try:
            numero = int(numero)
            if not NumeroSorteado.query.filter_by(numero=numero).first():
                db.session.add(NumeroSorteado(numero=numero))
                db.session.commit()

                # Verificar se alguma cartela venceu
                numeros_sorteados = {n.numero for n in NumeroSorteado.query.all()}
                for cartela in Cartela.query.all():
                    faltando = set(cartela.numeros) - numeros_sorteados
                    if len(faltando) == 0:  # Vencedor encontrado
                        return render_template("vencedor.html", identificacao=cartela.identificacao)
            else:
                flash("Número já foi sorteado!", "danger")
        except ValueError:
            flash("Por favor, insira um número inteiro válido.", "danger")

    return redirect(url_for("main.index"))

@main_bp.route("/adicionar_cartela", methods=["GET", "POST"])
def adicionar_cartela():
    if request.method == "POST":
        identificacao = request.form.get("identificacao")
        numeros = request.form.get("numeros")
        if identificacao and numeros:
            numeros = [int(n) for n in numeros.split(",")]
            nova_cartela = Cartela(identificacao=identificacao, numeros=numeros)
            db.session.add(nova_cartela)
            db.session.commit()
        return redirect(url_for("main.adicionar_cartela"))

    cartelas = Cartela.query.all()
    # Formatar os números para o template
    for cartela in cartelas:
        cartela.numeros_formatados = ", ".join(map(str, cartela.numeros))

    return render_template("adicionar_cartela.html", cartelas=cartelas)

@main_bp.route("/editar_cartela/<int:cartela_id>", methods=["GET", "POST"])
def editar_cartela(cartela_id):
    cartela = Cartela.query.get_or_404(cartela_id)
    if request.method == "POST":
        cartela.identificacao = request.form.get("identificacao")
        cartela.numeros = [int(n) for n in request.form.get("numeros").split(",")]
        db.session.commit()
        return redirect(url_for("main.adicionar_cartela"))

    # Formatar os números para exibição no formulário
    cartela.numeros_formatados = ", ".join(map(str, cartela.numeros))
    return render_template("editar_cartela.html", cartela=cartela)

@main_bp.route("/excluir_cartela/<int:cartela_id>", methods=["POST"])
def excluir_cartela(cartela_id):
    cartela = Cartela.query.get_or_404(cartela_id)
    db.session.delete(cartela)
    db.session.commit()
    return redirect(url_for("main.adicionar_cartela"))

@main_bp.route("/reiniciar", methods=["POST"])
def reiniciar():
    deletar_tudo(db)
    return redirect(url_for("main.index"))
