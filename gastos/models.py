from django.db import models


class Grupo(models.Model):
    nombre = models.CharField(max_length=80)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre


class Miembro(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='miembros')
    nombre = models.CharField(max_length=60)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='gastos')
    descripcion = models.CharField(max_length=120)
    monto = models.PositiveIntegerField(help_text='En pesos (COP)')
    pagado_por = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='pagos')
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f'{self.descripcion} (${self.monto})'
