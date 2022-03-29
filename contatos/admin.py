from django.contrib import admin
from .models import Contato, Categoria


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria', 'mostrar')
    list_display_links = ('id', 'nome')
    list_filter = ('categoria',)
    list_per_page = 5
    search_fields = ('nome', 'email')
    list_editable = ('mostrar',)

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
