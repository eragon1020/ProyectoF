from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('grupo/<int:grupo_id>/', views.grupo, name='grupo'),
    path('sugerencias/', views.sugerencias, name='sugerencias'),
    path('sugerencias/crear/', views.sugerencia_crear, name='sugerencia-crear'),
    path('sugerencias/<str:sid>/borrar/', views.sugerencia_borrar, name='sugerencia-borrar'),
    path('sugerencias/<str:sid>/actualizar/', views.sugerencia_actualizar, name='sugerencia-actualizar'),
    path('asistente/', views.asistente, name='asistente'),
    path('grupo/<int:grupo_id>/borrar/', views.borrar_grupo, name='borrar-grupo'),
    path('gasto/<int:gasto_id>/borrar/', views.borrar_gasto, name='borrar-gasto'),
]
