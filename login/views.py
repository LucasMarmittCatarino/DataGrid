from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import AdminCreateForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        verificacao_user = authenticate(request, username=username, password=password)

        if verificacao_user is not None:
            login(request, verificacao_user)
            return redirect('usuarios')  
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def cadastrar_admin(request):
    if request.method == 'POST':
        form = AdminCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
    else:
        form = AdminCreateForm()
    
    dados = {
        'form': form
     }
    return render(request, 'login/cadastro_admin.html', dados)


