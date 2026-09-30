"""Cálculo de saldos y de quién le paga a quién (gasto dividido en partes iguales)."""


def calcular_saldos(grupo):
    """Devuelve {miembro: saldo}. Positivo = le deben; negativo = debe."""
    miembros = list(grupo.miembros.all())
    if not miembros:
        return {}
    total = sum(g.monto for g in grupo.gastos.all())
    parte = total / len(miembros)
    pagado = {m.id: 0 for m in miembros}
    for g in grupo.gastos.all():
        pagado[g.pagado_por_id] += g.monto
    return {m: round(pagado[m.id] - parte) for m in miembros}


def calcular_pagos(saldos):
    """Lista mínima (aprox.) de transferencias [(deudor, acreedor, monto)]."""
    deben = sorted([[m, -s] for m, s in saldos.items() if s < 0], key=lambda x: -x[1])
    reciben = sorted([[m, s] for m, s in saldos.items() if s > 0], key=lambda x: -x[1])
    pagos = []
    i = j = 0
    while i < len(deben) and j < len(reciben):
        monto = min(deben[i][1], reciben[j][1])
        if monto > 0:
            pagos.append((deben[i][0], reciben[j][0], monto))
        deben[i][1] -= monto
        reciben[j][1] -= monto
        if deben[i][1] == 0:
            i += 1
        if reciben[j][1] == 0:
            j += 1
    return pagos
