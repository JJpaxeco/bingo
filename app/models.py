from app import db

class NumeroSorteado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)

class Cartela(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificacao = db.Column(db.String(10), unique=True, nullable=False)
    numeros = db.Column(db.PickleType, nullable=False)

    @staticmethod
    def verificar_proximos():
        proximos_de_vencer = []
        total_proximos = 0
        numeros_sorteados = [n.numero for n in NumeroSorteado.query.all()]
        for cartela in Cartela.query.all():
            faltam = set(cartela.numeros) - set(numeros_sorteados)
            if len(faltam) == 3:
                proximos_de_vencer.append(cartela.identificacao)
                total_proximos += 1
                if len(faltam) == 0:
                    return cartela.identificacao, "vencedor"
        return proximos_de_vencer, total_proximos


def deletar_tudo(db):
    db.session.query(NumeroSorteado).delete()
    db.session.query(Cartela).delete()
    db.session.commit()