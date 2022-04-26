from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('person_connection', views.person_connection, name='person_connection'),
    path('/graph_person', views.person_connection, name='graph_person'),
    path('/company_connection', views.company_connection, name='company_connection'),

]