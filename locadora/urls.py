from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('usuarios/inativos/', views.usuarios_inativos, name='usuarios_inativos'),
    path('usuarios/ativar/<int:id>/', views.ativar_usuario, name='ativar_usuario'),
    path('usuarios/ordenar/<campo>/', views.ordenar_usuarios, name='ordenar_usuarios'),
    path('usuarios/ordenar/inativos/<campo>/', views.ordenar_usuarios_inativos, name='ordenar_usuarios_inativos'),
    path('usuario/<int:usuario_id>/', views.detalhes_cliente, name='detalhes_cliente'),

    path('equipamentos/', views.equipamentos, name='equipamentos'),
    path('equipamentos/indisponiveis/', views.equipamentos_indisponiveis, name='equipamentos_indisponiveis'),
    path('equipamentos/alugados/', views.equipamentos_alugados, name='equipamentos_alugados'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('editar_equipamento/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('excluir_equipamento/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    path('remover_manutencao/<int:id>/', views.remover_manutencao, name='remover_manutencao'),
    path('relatorio/equipamento/<int:id>/', views.relatorio_equipamento, name='relatorio_equipamento'),
    path('disponibilizar_equipamento/<int:id>/', views.disponibilizar_equipamento, name='disponibilizar_equipamento'),
]
