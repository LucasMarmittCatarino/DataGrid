from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('equipamentos/', views.equipamentos, name='equipamentos'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('editar_equipamento/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('excluir_equipamento/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('usuarios/inativos/', views.usuarios_inativos, name='usuarios_inativos'),
    path('usuarios/ativar/<int:id>/', views.ativar_usuario, name='ativar_usuario'),
    path('usuarios/ordenar/<campo>/', views.ordenar_usuarios, name='ordenar_usuarios'),
    path('usuarios/ordenar/inativos/<campo>/', views.ordenar_usuarios_inativos, name='ordenar_usuarios_inativos'),
    path('remover_manutencao/<int:id>/', views.remover_manutencao, name='remover_manutencao'),
]
