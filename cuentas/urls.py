from django.urls import path
from .views import register, iniciosesion, exit
from . import views

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', iniciosesion, name="login"),
    path('logout/', exit, name="logout"),
    path('perfil/', views.perfil, name='perfil'),
    path('sin_permiso/', views.sin_permiso, name='sin_permiso'),

]

