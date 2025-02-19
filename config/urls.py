from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/', views.redirecionar, name='task_geral'),
    path('task/<int:task_id>', views.redirecionar, name='task_especifico')
]
