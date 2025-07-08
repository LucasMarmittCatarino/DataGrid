from django import forms
from .models import Equipamento, Usuario, Manutencao
from django.db import models
from django.utils import timezone

class EquipamentoCreateForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'modelo', 'numero_serie', 'categoria', 'fabricante', 'foto']

class EquipamentoUpdateForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['foto', 'nome', 'modelo', 'numero_serie', 'categoria', 'fabricante', 'em_manutencao']


class UsuarioForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Usuario
        fields = [
            'nome', 'data_nascimento', 'cpf', 'genero', 'estado_civil',
            'escolaridade', 'equipamento', 'telefone',
            'cidade', 'bairro', 'rua', 'numero', 'complemento',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        equipamento_atual = self.instance.equipamento if self.instance and self.instance.equipamento else None

        equipamentos_disponiveis = Equipamento.objects.filter(status='DISPONIVEL')

        if equipamento_atual:
            equipamentos_disponiveis = Equipamento.objects.filter(
                models.Q(status='DISPONIVEL') | models.Q(id=equipamento_atual.id)
            )

        self.fields['equipamento'].queryset = equipamentos_disponiveis

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['descricao']

    def clean(self):
        cleaned_data = super().clean()
        descricao = cleaned_data.get('descricao')

        if not descricao:
            raise forms.ValidationError("A descrição da manutenção é obrigatória.")
        return cleaned_data

