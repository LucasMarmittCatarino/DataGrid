from django.db import models
from stdimage.models import StdImageField

GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('NB', 'Não-binário'),
    ('O', 'Outro'),
]

ESTADO_CIVIL_CHOICES = [
    ('S', 'Solteiro'),
    ('C', 'Casado'),
    ('D', 'Divorciado'),
    ('V', 'Viúvo'),
]

ESCOLARIDADE_CHOICES = [
    ('fun', 'Fundamental'),
    ('med', 'Médio'),
    ('sup', 'Superior'),
    ('pos', 'Pós-graduação'),
    ('mes', 'Mestrado'),
    ('dou', 'Doutorado'),
]

STATUS_CHOICES = [
    ('DISPONIVEL', 'Disponível'),
    ('INDISPONIVEL', 'Indisponível'),
    ('ALUGADO', 'Alugado'),
]

class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    categoria = models.CharField(max_length=100, blank=True, null=True)
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    em_manutencao = models.BooleanField(default=False)
    data_alugado = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.formatar_nome_equipamento(self.nome)
        super().save(*args, **kwargs)

    def formatar_nome_equipamento(self, nome):
        partes = nome.lower().split()
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e',
                      'em', 'a', 'o', 'as', 'os', 'para', 'com']

        return ' '.join([
            p if p in minusculas else p.capitalize()
            for p in partes
        ])


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    foto = StdImageField(
        upload_to='fotos/equipamentos',
        variations={'thumb': (150, 150), 'medium': (300, 300)},
        blank=True,
        null=True
    )
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES)
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL_CHOICES)
    escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    telefone = models.CharField(max_length=15, blank=True, null=True)

    cidade = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.formatar_nome(self.nome)
        super().save(*args, **kwargs)

    def formatar_nome(self, nome):
        partes = nome.lower().split()
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e']
        return ' '.join([p if p in minusculas else p.capitalize() for p in partes])

class Manutencao(models.Model):
    equipamento = models.OneToOneField(Equipamento, on_delete=models.CASCADE, related_name='manutencao')
    data = models.DateField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.equipamento.nome} - {self.data}'