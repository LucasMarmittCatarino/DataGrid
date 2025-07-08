from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Usuario, Equipamento
from .forms import EquipamentoForm, UsuarioForm, ManutencaoForm
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import RestrictedError
from django.utils import timezone
from django.db import models

ORDENACAO_USUARIOS_LOOKUP = {
    'equipamento': 'equipamento__nome',
    'nome': 'nome',
    'genero': 'genero',
    'escolaridade': 'escolaridade',
    'estado_civil': 'estado_civil',
    'data_nascimento': 'data_nascimento',
    'telefone': 'telefone'
}

@login_required
def usuarios(request):
    query = request.GET.get('busca', '')
    if query:
        usuarios = Usuario.objects.filter(ativo=True, nome__icontains=query)
    else:
        usuarios = Usuario.objects.filter(ativo=True)
    dados = {
        'usuarios': usuarios,
        'ativos': True,
        'query': query,
    }
    return render(request, 'locadora/lista_clientes.html', dados)

@login_required
def usuarios_inativos(request):
    query = request.GET.get('busca', '')
    if query:
        usuarios = Usuario.objects.filter(ativo=False, nome__icontains=query)
    else:
        usuarios = Usuario.objects.filter(ativo=False)

    dados = {
        'usuarios': usuarios,
        'ativos': False,
        'query': query
    }
    return render(request, 'locadora/lista_clientes.html', dados)

@login_required
def equipamentos(request):
    query = request.GET.get('busca', '')

    equipamentos = Equipamento.objects.filter(
        status='DISPONIVEL',
        em_manutencao=False
    )

    if query:
        equipamentos = equipamentos.filter(
            models.Q(nome__icontains=query) |
            models.Q(modelo__icontains=query) |
            models.Q(numero_serie__icontains=query) |
            models.Q(categoria__icontains=query) |
            models.Q(fabricante__icontains=query)
        )

    dados = {
        'equipamentos': equipamentos,
        'query': query,
    }

    return render(request, 'locadora/lista_equipamentos.html', dados)



@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save()
            if cliente.equipamento:
                cliente.equipamento.status = 'ALUGADO'
                if not cliente.equipamento.data_alugado:
                    cliente.equipamento.data_alugado = timezone.now().date()
                cliente.equipamento.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm()

    dados = {
        'form': form,
    }
    return render(request, 'locadora/cadastrar_cliente.html', dados)


@login_required
def cadastrar_equipamento(request):

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('equipamentos')
    else:
        form = EquipamentoForm()
        dados = {
            'form': form,
        }
    return render(request, 'locadora/cadastrar_equipamento.html', dados)

@login_required
def editar_cliente(request, id):

    try:
        usuario = Usuario.objects.get(id=id)
    except:
        return redirect('usuarios')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            cliente = form.save()

            if cliente.equipamento:
                cliente.equipamento.status = 'ALUGADO'
                if not cliente.equipamento.data_alugado:
                    cliente.equipamento.data_alugado = timezone.now().date()
                cliente.equipamento.save()

            return redirect('usuarios')


    form = UsuarioForm(instance=usuario)

    dados = {
        'form': form,
        'usuario': usuario,
    }

    return render(request, 'locadora/editar_cliente.html', dados)



@login_required
def editar_equipamento(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id)
    except Equipamento.DoesNotExist:
        return redirect('equipamentos')

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES, instance=equipamento)
        manutencao_form = ManutencaoForm(
            request.POST,
            instance=equipamento.manutencao if hasattr(equipamento, 'manutencao') else None
        )

        if form.is_valid():
            em_manutencao = form.cleaned_data['em_manutencao']
            status = form.cleaned_data['status']

            if em_manutencao and status == 'ALUGADO':
                messages.error(request, "O equipamento não pode ser alugado enquanto estiver em manutenção.")
                dados = {
                    'form': form,
                    'manutencao_form': manutencao_form,
                    'equipamento': equipamento,
                }
                return render(request, 'locadora/editar_equipamento.html', dados)

            equipamento = form.save(commit=False)

            if status == 'ALUGADO' and not equipamento.data_alugado:
                equipamento.data_alugado = timezone.now().date()
            elif status != 'ALUGADO':
                equipamento.data_alugado = None


            equipamento.save()

            if em_manutencao:
                if manutencao_form.is_valid():
                    manut = manutencao_form.save(commit=False)
                    manut.equipamento = equipamento
                    manut.save()
            else:
                if hasattr(equipamento, 'manutencao'):
                    equipamento.manutencao.delete()

            return redirect('equipamentos')

    else:
        form = EquipamentoForm(instance=equipamento)
        manutencao_form = ManutencaoForm(
            instance=equipamento.manutencao if hasattr(equipamento, 'manutencao') else None
        )

    dados = {
        'form': form,
        'manutencao_form': manutencao_form,
        'equipamento': equipamento,
    }
    return render(request, 'locadora/editar_equipamento.html', dados)


@login_required
def excluir_equipamento(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id)

        usuarios_vinculados = Usuario.objects.filter(equipamento=equipamento)
        for usuario in usuarios_vinculados:
            usuario.equipamento = None
            usuario.save()

        equipamento.delete()
        messages.success(request, "Equipamento excluído com sucesso.")
    except Equipamento.DoesNotExist:
        messages.error(request, "Equipamento não encontrado.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")

    return redirect('equipamentos')


@login_required
def excluir_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
        usuario.ativo = False
        usuario.save()
        messages.success(request, "Usuario excluído com sucesso.")
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario não encontrado.")

    return redirect('usuarios')


def ativar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario não encontrado.")
        return redirect('usuarios_inativos')

    if usuario.ativo == False:
        usuario.ativo = True
        usuario.save()
        messages.success(request, "Usuario reativado com sucesso.")

    else:
        messages.info(request, "O usuario já está ativo.")

    return redirect('usuarios_inativos')

@login_required
def ordenar_usuarios(request, campo):
    campo_ordenacao = ORDENACAO_USUARIOS_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    usuarios = Usuario.objects.filter(ativo=True)

    if busca:
        usuarios = usuarios.filter(nome__icontains=busca)

    usuarios = usuarios.order_by(campo_ordenacao)
    dados = {
        'usuarios': usuarios,
        'ativos': True,
        'query': busca,
    }
    return render(request, 'locadora/lista_clientes.html', dados)

@login_required
def ordenar_usuarios_inativos(request, campo):
    campo_ordenacao = ORDENACAO_USUARIOS_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    usuarios = Usuario.objects.filter(ativo=False)

    if busca:
        usuarios = Usuario.objects.filter(nome__icontains=busca)

    usuarios = usuarios.order_by(campo_ordenacao)
    dados = {
        'usuarios': usuarios,
        'ativos': False,
        'query': busca,
    }
    return render(request, 'locadora/lista_clientes.html', dados)

@require_POST
@login_required
def remover_manutencao(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id)
        if hasattr(equipamento, 'manutencao'):
            equipamento.manutencao.delete()
        equipamento.em_manutencao = False
        equipamento.save()
        messages.success(request, "Equipamento removido da manutenção com sucesso.")
    except Equipamento.DoesNotExist:
        messages.error(request, "Equipamento não encontrado.")
    return redirect('equipamentos')

@login_required
def detalhes_cliente(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario não encontrado.")
        return redirect('usuarios')
    
    dados = {
        'usuario': usuario,
    }

    return render(request, 'locadora/detalhes_cliente.html', dados)

@login_required
def equipamentos_alugados(request):
    query = request.GET.get('busca', '')
    equipamentos = Equipamento.objects.filter(status='ALUGADO')

    if query:
        equipamentos = equipamentos.filter(
            models.Q(nome__icontains=query) |
            models.Q(modelo__icontains=query) |
            models.Q(numero_serie__icontains=query) |
            models.Q(categoria__icontains=query) |
            models.Q(fabricante__icontains=query)
        )

    dados = {
        'equipamentos': equipamentos,
        'query': query,
    }
    return render(request, 'locadora/lista_equipamentos_alugados.html', dados)

@login_required
def equipamentos_indisponiveis(request):
    query = request.GET.get('busca', '')

    equipamentos = Equipamento.objects.filter(
        models.Q(status='INDISPONIVEL') | models.Q(em_manutencao=True)
    )

    if query:
        equipamentos = equipamentos.filter(
            models.Q(nome__icontains=query) |
            models.Q(modelo__icontains=query) |
            models.Q(numero_serie__icontains=query) |
            models.Q(categoria__icontains=query) |
            models.Q(fabricante__icontains=query)
        )

    dados = {
        'equipamentos': equipamentos,
        'query': query,
    }

    return render(request, 'locadora/lista_equipamentos_indisponiveis.html', dados)

@login_required
def relatorio_equipamento(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id, status='ALUGADO')
    except Equipamento.DoesNotExist:
        messages.error(request, "Equipamento não encontrado ou não está alugado.")
        return redirect('equipamentos_alugados')

    cliente = Usuario.objects.filter(equipamento=equipamento, ativo=True).first()

    dados = {
        'equipamento': equipamento,
        'cliente': cliente,
    }

    return render(request, 'locadora/relatorio_equipamento.html', dados)

