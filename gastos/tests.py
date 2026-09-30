from django.test import TestCase
from django.urls import reverse

from .logic import calcular_pagos, calcular_saldos
from .models import Gasto, Grupo, Miembro


class CuentasTests(TestCase):
    def setUp(self):
        self.g = Grupo.objects.create(nombre='Viaje')
        self.a = Miembro.objects.create(grupo=self.g, nombre='Ana')
        self.b = Miembro.objects.create(grupo=self.g, nombre='Beto')
        self.c = Miembro.objects.create(grupo=self.g, nombre='Cami')
        Gasto.objects.create(grupo=self.g, descripcion='Hotel', monto=90000, pagado_por=self.a)
        Gasto.objects.create(grupo=self.g, descripcion='Comida', monto=30000, pagado_por=self.b)

    def test_saldos_y_pagos(self):
        saldos = calcular_saldos(self.g)
        self.assertEqual(saldos[self.a], 50000)
        self.assertEqual(saldos[self.b], -10000)
        self.assertEqual(saldos[self.c], -40000)
        pagos = calcular_pagos(saldos)
        self.assertEqual(sum(p[2] for p in pagos), 50000)

    def test_flujo_web(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        r = self.client.get(reverse('grupo', args=[self.g.id]))
        self.assertContains(r, '90.000')
        r = self.client.post(reverse('grupo', args=[self.g.id]),
                             {'agregar_gasto': '1', 'g-descripcion': 'Taxi', 'g-monto': 12000, 'g-pagado_por': self.c.id})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.g.gastos.count(), 3)
        self.client.post(reverse('borrar-grupo', args=[self.g.id]))
        self.assertEqual(Grupo.objects.count(), 0)
