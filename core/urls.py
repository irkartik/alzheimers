from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addPerson, name="addPerson"),
    path('compare/', views.comparePerson, name="comparePerson"),
    path('getall/', views.getAll, name="getAll"),
]