from django.contrib import admin
from .models import Ativo, TunelDePreco, ConfiguracaoChecagem

admin.site.register(Ativo)
admin.site.register(TunelDePreco)
admin.site.register(ConfiguracaoChecagem)
