from django import forms
from .models import Equipamento, Usuario, Manutencao


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [ 'nome', 'modelo', 'numero_serie', 'status', 'categoria', 'fabricante', 'em_manutencao', 'data_alugado']


class UsuarioForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Usuario
        fields = [
            'foto', 'nome', 'data_nascimento', 'cpf', 'genero', 'estado_civil',
            'escolaridade', 'equipamento', 'telefone',
            'cidade', 'bairro', 'rua', 'numero', 'complemento'
        ]

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['data', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }

