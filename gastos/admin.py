from django.contrib import admin

from .models import Gasto, Grupo, Miembro

admin.site.register([Grupo, Miembro, Gasto])
