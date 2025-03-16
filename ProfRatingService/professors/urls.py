from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view, name='view'),
    path('list/', views.list, name='list'),
    path('average/<str:professorId>/<str:moduleId>/', views.average, name='average'),
    path('rate/', views.rate, name='rate'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('register/', views.register, name='register'),
]