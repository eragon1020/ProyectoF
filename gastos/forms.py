from django import forms

from .models import Gasto, Grupo, Miembro


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Viaje a Villa de Leyva'})}


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'})}


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descripcion', 'monto', 'pagado_por']
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Mercado'}),
            'monto': forms.NumberInput(attrs={'min': 1, 'placeholder': '0'}),
        }

    def __init__(self, *args, grupo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pagado_por'].queryset = grupo.miembros.all()
        self.fields['pagado_por'].label = '¿Quién pagó?'
        self.fields['monto'].label = 'Monto (COP)'

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto < 1:
            raise forms.ValidationError('El monto debe ser mayor a 0.')
        return monto


class PreguntaForm(forms.Form):
    pregunta = forms.CharField(
        label='',
        max_length=300,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: ¿Cómo se dividen los gastos entre los miembros?',
        }),
    )
