from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login realizado com sucesso!')
        return redirect('dashboard')



def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    print(request.method)
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    campos = {
        'nome': request.POST.get('nome'),
        'sobrenome': request.POST.get('sobrenome'),
        'email': request.POST.get('email'),
        'usuario': request.POST.get('usuario'),
        'senha': request.POST.get('senha'),
        'senha2': request.POST.get('senha2'),
    }
    for campo, valor in campos.items():
        if not valor:
            messages.error(request, f'Todos os campos devem ser preenchidos.')
            return render(request, 'accounts/register.html')

    try:
        validate_email(campos['email'])
    except:
        messages.error(request, f'Email inválido!')
        return render(request, 'accounts/register.html')

    if len(campos['senha']) < 6:
        messages.error(request, f'A senha precisa ter mais de 6 caracteres!')
        return render(request, 'accounts/register.html')

    if campos['senha'] != campos['senha2']:
        messages.error(request, f'As senhas precisam ser iguais')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=campos['usuario']).exists():
        messages.error(request, f'Usuário já cadastrado!')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=campos['email']).exists():
        messages.error(request, f'Email já cadastrado!')
        return render(request, 'accounts/register.html')

    user = User.objects.create_user(username=campos['usuario'], email=campos['email'], password=campos['senha'],
                                    first_name=campos['nome'], last_name=campos['sobrenome'])
    user.save()
    messages.success(request, 'Registrado com Sucesso!')

    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar o formulário.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, 'Formulário enviado com sucesso!')
    return render(request, 'accounts/dashboard.html', {'form': FormContato()})
