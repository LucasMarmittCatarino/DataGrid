from django.contrib import admin
from .models import Equipamento, Usuario

# Register your models here.

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'equipamento')
    search_fields = ('nome',)
    list_filter = ('equipamento',)
