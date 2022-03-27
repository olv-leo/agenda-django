from django.contrib import admin
from .models import Contato, Categoria


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria')
    list_display_links = ('id', 'nome')
    list_filter = ('nome', 'categoria')
    list_per_page = 10
    search_fields = ('nome', 'email')


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
