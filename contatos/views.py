from django.shortcuts import render, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def ver_contato(request, contato_id):
    try:
        contato = Contato.objects.get(id=contato_id)
    except:
        messages.add_message(
            request,
            messages.WARNING,
            'O contato procurado não foi encontrado.'
        )
        return redirect('index')
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Campo de pesquisa não pode ficar vazio.'
        )
        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    paginator = Paginator(contatos, 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
