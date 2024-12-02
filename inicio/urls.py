from django.urls import path
from .views import vistaIndex
urlpatterns=[
    path('',vistaIndex,name="Inicio")
    
]